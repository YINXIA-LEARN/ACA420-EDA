"""Four-marker displacement prototype. Run with Python 3.12: python run_model.py"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


NAMES = ("R", "P1", "P2", "P3")
INITIAL = np.array([[45, 110], [112, 110], [181, 110], [250, 110]], dtype=float)
FPS = 30.0
SCALE_MM_PER_PX = 0.10  # Synthetic demo only; replace with measured calibration.


def make_demo_frame(frame_id: int, width=320, height=220):
    """Known ground truth, shared camera translation, and an intentional occlusion."""
    t = frame_id / FPS
    shake = np.array([2.0 * np.sin(2 * np.pi * 0.29 * t),
                      2.5 * np.sin(2 * np.pi * 0.37 * t)])
    amplitudes = (0.0, 2.0, 4.0, 7.0)
    centers = INITIAL.copy()
    centers += shake
    for i in range(1, 4):
        centers[i, 1] += amplitudes[i] * np.sin(2 * np.pi * 1.2 * t)
    frame = np.full((height, width, 3), 25, dtype=np.uint8)
    for i, center in enumerate(centers):
        if i == 2 and 48 <= frame_id <= 58:
            continue
        cv2.circle(frame, tuple(np.rint(center).astype(int)), 5, (245, 245, 245), -1)
    return frame, centers, (48 <= frame_id <= 58)


def locate_marker(gray: np.ndarray, predicted: np.ndarray, radius=18):
    """Binary centroid inside a fixed ROI, matching a simple streaming RTL design."""
    x, y = map(int, np.rint(predicted))
    x0, x1 = max(0, x - radius), min(gray.shape[1], x + radius + 1)
    y0, y1 = max(0, y - radius), min(gray.shape[0], y + radius + 1)
    roi = gray[y0:y1, x0:x1]
    mask = cv2.threshold(roi, 150, 255, cv2.THRESH_BINARY)[1]
    count = int(cv2.countNonZero(mask))
    if not 35 <= count <= 130:
        return None, count
    m = cv2.moments(mask, binaryImage=True)
    if m["m00"] == 0:
        return None, count
    return np.array([x0 + m["m10"] / m["m00"], y0 + m["m01"] / m["m00"]]), count


def process_frame(frame: np.ndarray, predicted: np.ndarray):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    points, areas = [], []
    for p in predicted:
        point, area = locate_marker(gray, p)
        points.append(point)
        areas.append(area)
    return points, areas


def run_demo(output: Path, count=150):
    output.mkdir(parents=True, exist_ok=True)
    predicted = INITIAL.copy()
    origin = None
    rows = []
    errors = []
    for k in range(count):
        frame, truth, occluded = make_demo_frame(k)
        points, areas = process_frame(frame, predicted)
        if origin is None and all(p is not None for p in points):
            origin = np.stack(points)
        for i, p in enumerate(points):
            if p is not None:
                predicted[i] = p
            valid = p is not None and points[0] is not None
            corrected = np.array([np.nan, np.nan])
            raw = np.array([np.nan, np.nan])
            if valid:
                raw = (p - origin[i]) * SCALE_MM_PER_PX
                corrected = ((p - origin[i]) - (points[0] - origin[0])) * SCALE_MM_PER_PX
                if i > 0 and not occluded:
                    true_disp = (truth[i] - truth[0] - (INITIAL[i] - INITIAL[0])) * SCALE_MM_PER_PX
                    errors.append(abs(corrected[1] - true_disp[1]))
            rows.append(dict(frame_id=k, time_s=f"{k/FPS:.4f}", target=NAMES[i],
                             valid=int(valid), area=areas[i],
                             x_px=f"{p[0]:.4f}" if p is not None else "",
                             y_px=f"{p[1]:.4f}" if p is not None else "",
                             raw_dy_mm=f"{raw[1]:.4f}" if valid else "",
                             corrected_dx_mm=f"{corrected[0]:.4f}" if valid else "",
                             corrected_dy_mm=f"{corrected[1]:.4f}" if valid else ""))
        if k in (0, 52, count - 1):
            cv2.imwrite(str(output / f"frame_{k:03}.png"), frame)
    with (output / "measurements.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    for name in NAMES[1:]:
        rr = [r for r in rows if r["target"] == name]
        t = [float(r["time_s"]) for r in rr]
        axes[0].plot(t, [float(r["corrected_dy_mm"]) if r["valid"] else np.nan for r in rr], label=name)
    rr = [r for r in rows if r["target"] == "P3"]
    axes[1].plot([float(r["time_s"]) for r in rr], [float(r["raw_dy_mm"]) for r in rr], label="P3 raw")
    axes[1].plot([float(r["time_s"]) for r in rr], [float(r["corrected_dy_mm"]) for r in rr], label="P3 reference corrected")
    axes[0].set_ylabel("Corrected displacement (mm)")
    axes[1].set_ylabel("Displacement (mm)")
    axes[1].set_xlabel("Time (s)")
    for ax in axes:
        ax.grid(True)
        ax.legend()
    fig.tight_layout()
    fig.savefig(output / "displacement.png", dpi=160)
    plt.close(fig)
    lost = sum(r["valid"] == 0 for r in rows if r["target"] == "P2")
    print(f"Generated {count} synthetic frames; P2 invalid frames: {lost}")
    print(f"Synthetic-only P1-P3 vertical MAE: {np.mean(errors):.4f} mm")
    print(f"Output: {output.resolve()}")
    assert lost == 11, "Occlusion must be rejected rather than silently filled."
    assert np.mean(errors) < 0.08, "Synthetic tracking deviation is unexpectedly large."


def run_image(path: Path, output: Path):
    frame = cv2.imread(str(path))
    if frame is None:
        raise SystemExit(f"Cannot read image: {path}")
    print("Real-image mode is diagnostic only. Coordinates are relative to original 320x220 demo layout.")
    print("Use --demo first; real image ROI configuration will require the actual camera layout.")
    points, areas = process_frame(frame, INITIAL)
    for name, p, area in zip(NAMES, points, areas):
        print(name, "lost" if p is None else tuple(np.round(p, 2)), "area", area)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run reproducible synthetic experiment (default).")
    parser.add_argument("--image", type=Path, help="Diagnostic read of one local image.")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "output")
    args = parser.parse_args()
    if args.image:
        run_image(args.image, args.output)
    else:
        run_demo(args.output)
