# Results and interpretation

At threshold 175, mean IoU and mean Dice are both **1.000** across 25 synthetic images. The perfect result follows from non-overlapping background and defect intensity ranges.

The threshold sweep provides the more informative result:

| Threshold range | Behavior |
|---|---|
| 120–140 | False-positive background pixels reduce IoU |
| 150–190 | Perfect separation on this generator |
| 200–230 | Increasing false negatives reduce recall and overlap |

![Threshold sensitivity](../results/threshold_sweep.svg)

At threshold 120, mean IoU is 0.051; at 150–190 it is 1.000; at 230 it falls to 0.134. This wide perfect interval measures generator separability, not general segmentation capability. A real study should compare this baseline with learned and adaptive methods under controlled domain shifts.

Exact values are in `threshold_sweep.csv`; per-image values are in `per_sample_metrics.csv`.
