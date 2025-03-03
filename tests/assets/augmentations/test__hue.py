import unittest
from CVAugmentor.assets.augmentations._hue import Hue
from PIL import Image, ImageChops


class TestHue(unittest.TestCase):

    def test_hue__shift_wrong__value_value__error(self):

        # Arrange
        hue_shift = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Hue(hue_shift=hue_shift)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Hue(1)(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Hue(1)
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()