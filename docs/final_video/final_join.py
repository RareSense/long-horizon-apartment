"""Final join of the clean episode (AI-operated): all rendered chain units in recording order, ending at the episode's
last item checkpoint (s4 0270_item_r83i1_sponges, rec frame 19979). Units recorded after that frame (bin-fix attempts)
are left out; the unit containing it is trimmed. Stream copy (no re-encode). Writes FINAL\episode_{room,head}_1080p.mp4."""
import json, os, re, subprocess

OUT = r"C:\Users\raresense\sim_home\final_video"
FIN = os.path.join(OUT, "FINAL"); os.makedirs(FIN, exist_ok=True)
RUN_ORDER = ["1120_181556_dex1_floor_final", "1121_021343_dex1_floor_final_s2",
             "1121_034845_dex1_floor_final_s3", "1121_123451_dex1_floor_final_s4"]
END_RUN, END_FRAME = "1121_123451_dex1_floor_final_s4", 19979

done = json.load(open(os.path.join(OUT, "done.json"), encoding="utf-8"))["units"]
units = []
for c in done:
    run, chunk, piece, a, b = c["key"].split("|")
    a, b = int(a), int(b)
    if c.get("status") not in ("ok", "FAILED") or not c.get("room") or not c.get("head"):
        continue
    if run == END_RUN and a > END_FRAME:
        continue
    units.append(dict(run=run, a=a, b=b, room=c["room"], head=c["head"], frames=c.get("frames")))
units.sort(key=lambda u: (RUN_ORDER.index(u["run"]), u["a"]))
work = os.path.join(FIN, "_work"); os.makedirs(work, exist_ok=True)
tot = 0
for cam in ("room", "head"):
    parts = []
    for u in units:
        p = u[cam]
        if not os.path.exists(p):
            raise SystemExit(f"missing chunk {p}")
        if u["run"] == END_RUN and u["a"] <= END_FRAME < u["b"]:      # trim the last unit at the episode end
            n = END_FRAME - u["a"] + 1
            q = os.path.join(work, f"{cam}_last_trim.mp4")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", p, "-frames:v", str(n), "-c:v", "libx264", "-crf", "20",
                            "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", q], check=True)
            p = q
        parts.append(p)
    lst = os.path.join(work, f"{cam}_list.txt")
    open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
    out = os.path.join(FIN, f"episode_{cam}_1080p.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    "-movflags", "+faststart", out], check=True)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "csv=p=0", out],
                       capture_output=True, text=True)
    print(cam, len(parts), "parts ->", out, r.stdout.strip())
