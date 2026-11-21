"""Floor navigation for the home tasks: a path for the walking base between things on the floor and furniture.

Obstacles are footprints (oriented rectangles) taken from the scene as it is now: furniture and walls (kept `r_body`
away from the pelvis: trunk, arms, a carried object) and small things lying on the floor (kept `r_foot` away: the feet
must not step on them). A* on a grid, then the path is shortened to straight legs. Pure numpy; nothing here moves
anything."""
from __future__ import annotations

import heapq
import math

import numpy as np


class Rect:
    """Footprint: centre (x, y), half sizes (hx, hy), yaw; `low` = a small thing on the floor (only the feet avoid it)."""

    def __init__(self, c, h, yaw=0.0, low=False, name=""):
        self.c = np.asarray(c, float)[:2]; self.h = np.asarray(h, float)[:2]; self.yaw = float(yaw); self.low = low; self.name = name
        cs, sn = math.cos(yaw), math.sin(yaw)
        self.R = np.array([[cs, -sn], [sn, cs]])

    def dist(self, P):
        """Distance from points P (n, 2) to the rectangle (0 inside)."""
        q = np.abs((np.asarray(P, float) - self.c) @ self.R) - self.h
        return np.linalg.norm(np.maximum(q, 0.0), axis=-1)


def min_rect(P, step_deg=3.0):
    """Smallest rectangle on the floor round the points P (n, 2 or 3): (centre, half sizes, yaw). A long thin thing lying
    askew (a 1 m stick) gets its own narrow footprint; its world-axis box would close half a room."""
    P = np.asarray(P, float)[:, :2]
    best = None
    for a in np.radians(np.arange(0.0, 90.0, step_deg)):
        cs, sn = math.cos(a), math.sin(a)
        R = np.array([[cs, -sn], [sn, cs]])
        Q = P @ R                                              # the points in the rectangle's own axes
        lo, hi = Q.min(0), Q.max(0)
        area = float((hi[0] - lo[0]) * (hi[1] - lo[1]))
        if best is None or area < best[0] - 1e-9:
            best = (area, R @ ((lo + hi) / 2), (hi - lo) / 2, float(a))
    return best[1], best[2], best[3]


class Grid:
    def __init__(self, lo, hi, rects, res=0.05, r_body=0.33, r_foot=0.20):
        self.lo = np.asarray(lo, float)[:2]; self.hi = np.asarray(hi, float)[:2]; self.res = res
        self.nx, self.ny = (np.ceil((self.hi - self.lo) / res).astype(int) + 1)
        X, Y = np.meshgrid(self.lo[0] + np.arange(self.nx) * res, self.lo[1] + np.arange(self.ny) * res, indexing="ij")
        P = np.stack([X.ravel(), Y.ravel()], 1)
        clear = np.full(len(P), 9.0)
        for r in rects:
            clear = np.minimum(clear, r.dist(P) - (r_foot if r.low else r_body))
        self.clear = clear.reshape(self.nx, self.ny)              # > 0: the pelvis may be here
        self.rects = rects

    def cell(self, p):
        i = np.clip(np.round((np.asarray(p, float)[:2] - self.lo) / self.res).astype(int), 0, [self.nx - 1, self.ny - 1])
        return int(i[0]), int(i[1])

    def point(self, c):
        return self.lo + np.array(c, float) * self.res

    def free(self, p, margin=0.0):
        i, j = self.cell(p)
        return bool(self.clear[i, j] > margin)

    def nearest_free(self, p, margin=0.0):
        ok = np.argwhere(self.clear > margin)
        if not len(ok):
            return None
        pts = self.lo + ok * self.res
        return pts[int(np.argmin(np.linalg.norm(pts - np.asarray(p, float)[:2], axis=1)))]

    def line_free(self, a, b, margin=0.0):
        a, b = np.asarray(a, float)[:2], np.asarray(b, float)[:2]
        n = max(2, int(np.linalg.norm(b - a) / (self.res * 0.5)) + 1)
        for t in np.linspace(0, 1, n):
            if not self.free(a + (b - a) * t, margin):
                return False
        return True

    def dist_from(self, start):
        """Walking distance [m] from `start` to every free cell (inf where it cannot be reached), one Dijkstra pass;
        kept for the last start asked. Lets many candidate goals be compared without a search each."""
        start = np.asarray(start, float)[:2]
        key = (round(float(start[0]), 2), round(float(start[1]), 2))
        if getattr(self, "_dist_key", None) == key:
            return self._dist
        s_free = start if self.free(start) else self.nearest_free(start)
        D = np.full((self.nx, self.ny), np.inf)
        if s_free is not None:
            s = self.cell(s_free); D[s] = float(np.linalg.norm(np.asarray(s_free) - start))
            pq = [(D[s], s)]
            nb = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 1.4142), (1, -1, 1.4142), (-1, 1, 1.4142), (-1, -1, 1.4142)]
            while pq:
                dc, c = heapq.heappop(pq)
                if dc > D[c]:
                    continue
                for dx, dy, w in nb:
                    n = (c[0] + dx, c[1] + dy)
                    if 0 <= n[0] < self.nx and 0 <= n[1] < self.ny and self.clear[n] > 0:
                        nd = dc + w * self.res
                        if nd < D[n]:
                            D[n] = nd; heapq.heappush(pq, (nd, n))
        self._dist_key, self._dist = key, D
        return D

    def reach_cost(self, start, goal, margin=-0.06):
        """Walking distance from start to a goal that may lie a little inside an inflated edge (a stance at furniture):
        distance to the nearest reachable cell within 0.25 m of it + the straight rest. inf when there is none."""
        D = self.dist_from(start)
        goal = np.asarray(goal, float)[:2]
        if not self.free(goal, margin):
            return float("inf")
        i, j = self.cell(goal); r = int(0.25 / self.res)
        best = float("inf")
        for a in range(max(i - r, 0), min(i + r + 1, self.nx)):
            for b in range(max(j - r, 0), min(j + r + 1, self.ny)):
                if np.isfinite(D[a, b]):
                    best = min(best, D[a, b] + float(np.linalg.norm(self.point((a, b)) - goal)))
        return best

    def plan(self, start, goal):
        """Way points from start to goal (both included), or None. A start or goal inside an inflated obstacle (the
        robot stands at furniture, the goal is a stance at it) is joined to the nearest free cell by a straight leg."""
        start, goal = np.asarray(start, float)[:2], np.asarray(goal, float)[:2]
        if self.line_free(start, goal):
            return [start, goal]
        s_free = start if self.free(start) else self.nearest_free(start)
        g_free = goal if self.free(goal) else self.nearest_free(goal)
        if s_free is None or g_free is None:
            return None
        s, g = self.cell(s_free), self.cell(g_free)
        open_ = [(0.0, s)]; came = {}; cost = {s: 0.0}
        nb = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 1.4142), (1, -1, 1.4142), (-1, 1, 1.4142), (-1, -1, 1.4142)]
        while open_:
            _, c = heapq.heappop(open_)
            if c == g:
                break
            for dx, dy, w in nb:
                n = (c[0] + dx, c[1] + dy)
                if not (0 <= n[0] < self.nx and 0 <= n[1] < self.ny) or self.clear[n] <= 0:
                    continue
                # keep a little further from things where there is room (cost falls with clearance up to 15 cm)
                nc = cost[c] + w * (1.0 + 2.0 * max(0.0, 0.15 - self.clear[n]) / 0.15)
                if nc < cost.get(n, 1e18):
                    cost[n] = nc; came[n] = c
                    heapq.heappush(open_, (nc + math.hypot(n[0] - g[0], n[1] - g[1]), n))
        if g not in came and g != s:
            return None
        cells = [g]
        while cells[-1] != s:
            cells.append(came[cells[-1]])
        pts = [self.point(c) for c in cells[::-1]]
        pts = [start] + pts + [goal] if not np.allclose(pts[-1], goal) or not np.allclose(pts[0], start) else pts
        # shorten: from each kept point jump to the farthest point seen along a free straight line
        out = [pts[0]]; i = 0
        while i < len(pts) - 1:
            j = len(pts) - 1
            while j > i + 1 and not self.line_free(pts[i], pts[j]):
                j -= 1
            out.append(pts[j]); i = j
        return out


def path_length(pts):
    return float(sum(np.linalg.norm(np.asarray(b) - np.asarray(a)) for a, b in zip(pts[:-1], pts[1:])))
