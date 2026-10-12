# Methodology

## Research question

How does a transparent intensity-threshold baseline behave on controlled synthetic surface-defect images, and how sensitive is it to threshold choice?

## Synthetic dataset

The deterministic generator uses seed 19 to create 25 grayscale images of size 96×96. Background pixels are sampled uniformly from 105–145. Each image contains one elliptical defect with random center and radii; defect pixels are sampled from 190–235. Ground-truth masks use 255 for defect and 0 for background.

## Segmentation and metrics

The main operating point labels pixels at or above 175 as defect. Evaluation reports intersection-over-union (IoU) and Dice coefficient. A sensitivity study repeats evaluation at thresholds from 120 through 230 in increments of 10. Per-image scores are exported to reveal variation hidden by the mean.

## Reproducibility

Run `python src/run_demo.py`, then `python -m unittest discover -s tests -v`. Inputs and results are regenerated deterministically without external packages. Portable graymap (`.pgm`) files preserve exact pixel values in a simple text representation.

## Limitations

The intensity ranges are deliberately separated, the defect geometry is simple, and there is no texture, illumination gradient, blur, occlusion, or annotation uncertainty. Production validation requires real labeled images and splits that prevent near-duplicate parts from crossing partitions.
