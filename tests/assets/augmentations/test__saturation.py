import unittest
from CVAugmentor.assets.augmentations._saturation import Saturation
from PIL import Image, ImageChops


class TestSaturation(unittest.TestCase):

    def test_saturation__factor_wrong__value_value__error(self):

        # Arrange
        saturation_factor = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Saturation(saturation_factor=saturation_factor)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Saturation(1)(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Saturation(1)
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()