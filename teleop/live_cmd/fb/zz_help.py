# Session helpers of the Fable blanket escalation (AI-operated). All names prefixed zz_.
zz_BL = "r117i1_blanket"
zz_LOOK_DIR = os.path.join(RUN, "look_fb")
os.makedirs(zz_LOOK_DIR, exist_ok=True)
zz_N = globals().get("zz_N") or [0]


def zz_hb():
    return laundry_body()


def zz_w():
    return GARMENTS[zz_BL]["w"]


def zz_uv():
    """Flat pattern coordinates [m] of every blanket particle, centred on the sheet's middle."""
    w_ = zz_w(); g_ = w_.garment(0)
    uv_ = w_._uv(g_) / CL.S
    return uv_ - (uv_.min(0) + uv_.max(0)) / 2


def zz_stat():
    w_ = zz_w(); P_ = w_.points(0)
    out_ = dict(state=state(), blanket=in_container(zz_BL, zz_hb()), box=[np.round(P_.min(0), 3).tolist(), np.round(P_.max(0), 3).tolist()],
                at_fingers={s_: w_.at_fingers(s_) for s_ in SIDES}, lock={s_: len(LOCK[s_][1]) for s_ in LOCK}, held=dict(HELD),
                jaw={s_: round(float(jaw(s_)), 4) for s_ in SIDES}, touch=contact_report(), asleep=bool(w_.asleep))
    return out_


def zz_img(paths, out_name):
    ims_ = [_Img.open(t_).resize((426, 320)) for t_ in paths]
    out_ = _Img.new("RGB", (426 * len(ims_), 320))
    for i_, im_ in enumerate(ims_):
        out_.paste(im_, (426 * i_, 0))
    zz_N[0] += 1
    p_ = os.path.join(zz_LOOK_DIR, f"{zz_N[0]:04d}_{out_name}.jpg")
    out_.save(p_, quality=82)
    return p_


def zz_look(at, tag, dist=1.0, h=0.5, dirs=(0.0, 90.0, 200.0), top=False):
    """Views of a world point from compass directions (deg, 0 = from the east) plus optionally straight down."""
    at = np.asarray(at, float); tmp_ = []
    for i_, a_ in enumerate(dirs):
        u_ = np.array([np.cos(np.radians(a_)), np.sin(np.radians(a_))])
        t_ = os.path.join(zz_LOOK_DIR, f"_z{i_}.jpg")
        close(t_, np.r_[at[:2] + u_ * dist, at[2] + h], at, f"{tag} from {int(a_)}")
        tmp_.append(t_)
    if top:
        t_ = os.path.join(zz_LOOK_DIR, "_zt.jpg")
        close(t_, at + np.array([0.02, 0.0, 1.1]), at - np.array([0, 0, 0.2]), f"{tag} top")
        tmp_.append(t_)
    return zz_img(tmp_, tag)


def zz_look_hamper(tag):
    cc_ = np.r_[obj_rect(zz_hb()).c, 0.6]
    return zz_look(cc_, tag, dist=1.15, h=0.75, dirs=(35.0, 150.0), top=True)


def zz_uv_of(idx):
    uv_ = zz_uv()
    return np.round(uv_[np.asarray(idx, int)], 3)


def zz_hang(side):
    P_ = zz_w().points(0)
    return round(float(pad_mid(side)[2] - P_[:, 2].min()), 3)


print("[zz] helpers loaded", flush=True)
