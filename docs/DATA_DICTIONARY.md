# Data dictionary

## Image encoding

The `.pgm` artifacts use ASCII PGM (`P2`), dimensions 96×96, and maximum value 255. `sample_input.pgm` is grayscale. Ground-truth and predicted masks use 0 for background and 255 for defect.

## Tabular results

`per_sample_metrics.csv` contains `sample`, `iou`, and `dice`. `threshold_sweep.csv` contains `threshold`, `mean_iou`, and `mean_dice`. `metrics.json` records the main operating point, aggregate scores, sample count, the first best sweep threshold, and the synthetic-data declaration.

IoU is `TP / (TP + FP + FN)`. Dice is `2TP / (2TP + FP + FN)`.
