import unittest
from CVAugmentor.assets.augmentations._cutout import Cutout
from PIL import Image, ImageChops


class TestCutout(unittest.TestCase):

    def test_max__size_wrong__value_value__error(self):

        # Arrange
        max_size = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Cutout(max_size=max_size)


    def test_max_count_wrong__value_value__error(self):

        # Arrange
        max_count = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Cutout(max_count=max_count)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Cutout(1, 1)(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Cutout(1, 1)
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()