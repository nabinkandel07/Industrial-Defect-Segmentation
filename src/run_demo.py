"""Threshold-based segmentation demo on synthetic industrial surfaces."""

import csv
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def write_pgm(path, pixels):
    height, width = len(pixels), len(pixels[0])
    body = "\n".join(" ".join(str(int(value)) for value in row) for row in pixels)
    path.write_text(f"P2\n{width} {height}\n255\n{body}\n", encoding="ascii")


def make_sample(rng, size=96):
    image = [[rng.randint(105, 145) for _ in range(size)] for _ in range(size)]
    mask = [[0 for _ in range(size)] for _ in range(size)]
    cx, cy = rng.randint(25, 70), rng.randint(25, 70)
    rx, ry = rng.randint(8, 16), rng.randint(5, 12)
    for y in range(size):
        for x in range(size):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                image[y][x] = rng.randint(190, 235)
                mask[y][x] = 255
    return image, mask


def segment(image, threshold=175):
    return [[255 if value >= threshold else 0 for value in row] for row in image]


def score(truth, predicted):
    tp = fp = fn = 0
    for truth_row, pred_row in zip(truth, predicted):
        for expected, actual in zip(truth_row, pred_row):
            tp += expected == 255 and actual == 255
            fp += expected == 0 and actual == 255
            fn += expected == 255 and actual == 0
    iou = tp / (tp + fp + fn)
    dice = 2 * tp / (2 * tp + fp + fn)
    return iou, dice


def threshold_sweep_svg(rows):
    width, height, margin = 720, 420, 50
    def point(threshold, value):
        x = margin + (threshold - rows[0][0]) / (rows[-1][0] - rows[0][0]) * (width - 2 * margin)
        y = height - margin - value * (height - 2 * margin)
        return f"{x:.1f},{y:.1f}"
    iou = " ".join(point(row[0], row[1]) for row in rows)
    dice = " ".join(point(row[0], row[2]) for row in rows)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/><text x="50" y="25" font-family="sans-serif" font-size="16">Segmentation threshold sensitivity</text>
<line x1="50" y1="370" x2="670" y2="370" stroke="#111"/><line x1="50" y1="50" x2="50" y2="370" stroke="#111"/>
<polyline points="{iou}" fill="none" stroke="#2563eb" stroke-width="3"/><polyline points="{dice}" fill="none" stroke="#dc2626" stroke-width="3"/>
<text x="560" y="25" fill="#2563eb" font-family="sans-serif">IoU</text><text x="610" y="25" fill="#dc2626" font-family="sans-serif">Dice</text></svg>'''


def main():
    RESULTS.mkdir(exist_ok=True)
    rng = random.Random(19)
    samples = []
    scores = []
    preview = None
    for index in range(25):
        image, truth = make_sample(rng)
        samples.append((image, truth))
        predicted = segment(image)
        scores.append(score(truth, predicted))
        if index == 0:
            preview = image, truth, predicted
    write_pgm(RESULTS / "sample_input.pgm", preview[0])
    write_pgm(RESULTS / "sample_ground_truth.pgm", preview[1])
    write_pgm(RESULTS / "sample_prediction.pgm", preview[2])
    with (RESULTS / "per_sample_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sample", "iou", "dice"])
        for index, row in enumerate(scores):
            writer.writerow([index, *row])
    sweep = []
    for threshold in range(120, 231, 10):
        threshold_scores = [score(truth, segment(image, threshold)) for image, truth in samples]
        sweep.append((threshold, sum(row[0] for row in threshold_scores) / len(threshold_scores), sum(row[1] for row in threshold_scores) / len(threshold_scores)))
    with (RESULTS / "threshold_sweep.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["threshold", "mean_iou", "mean_dice"])
        writer.writerows(sweep)
    metrics = {
        "samples": len(scores),
        "mean_iou": sum(x[0] for x in scores) / len(scores),
        "mean_dice": sum(x[1] for x in scores) / len(scores),
        "threshold": 175,
        "best_sweep_threshold": max(sweep, key=lambda row: row[1])[0],
        "data": "deterministic synthetic grayscale surfaces",
    }
    (RESULTS / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    (RESULTS / "threshold_sweep.svg").write_text(threshold_sweep_svg(sweep), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
