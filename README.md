# Industrial Defect Segmentation

A dependency-free image-segmentation baseline that generates synthetic grayscale surfaces with bright elliptical defects, applies fixed-threshold segmentation, and evaluates intersection-over-union and Dice score.

## Run

```bash
python src/run_demo.py
```

Python 3.10 or newer is recommended. No third-party packages are required. The generated PGM images can be opened by many image viewers and converted with common image tools.

## Reproducible demo result

| Metric | Result |
|---|---:|
| Synthetic images | 25 |
| Mean IoU | 1.000 |
| Mean Dice | 1.000 |
| Threshold | 175 / 255 |

The generator deliberately separates defect and background intensity ranges, so a threshold solves this toy dataset perfectly. This verifies the data, inference, and metric pipeline; it is not a claim about real inspection images.

Generated artifacts are committed under `results/`: `metrics.json`, per-sample scores, a threshold sweep with figure, a sample input, its ground truth, and its predicted mask in portable graymap format.

For academic review, see the detailed [methodology](docs/METHODOLOGY.md), [result interpretation](docs/RESULTS.md), and [data dictionary](docs/DATA_DICTIONARY.md). Validate the threshold and metric functions with `python -m unittest discover -s tests -v`.

## Next steps

Replace the generator with labeled production images, establish train/validation/test splits, train a U-Net-style model, and report per-defect metrics and inference latency.
