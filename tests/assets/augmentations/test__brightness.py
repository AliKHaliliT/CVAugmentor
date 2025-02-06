import unittest
from CVAugmentor.assets.augmentations._brightness import Brightness
from PIL import Image, ImageChops


class TestBrightness(unittest.TestCase):

    def test_brightness__factor_wrong__value_value__error(self):

        # Arrange
        brightness_factor = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Brightness(brightness_factor=brightness_factor)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Brightness(1)(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Brightness(1)
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()