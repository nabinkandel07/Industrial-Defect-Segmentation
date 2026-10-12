import unittest

from src.run_demo import score, segment


class SegmentationTests(unittest.TestCase):
    def test_threshold(self):
        self.assertEqual(segment([[100, 180]], threshold=175), [[0, 255]])

    def test_perfect_mask_metrics(self):
        mask = [[0, 255], [255, 0]]
        iou, dice = score(mask, mask)
        self.assertEqual(iou, 1.0)
        self.assertEqual(dice, 1.0)


if __name__ == "__main__":
    unittest.main()
