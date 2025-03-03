import unittest
from CVAugmentor.assets.augmentations._blur import Blur
from PIL import Image, ImageChops


class TestBlur(unittest.TestCase):

    def test_radius_wrong__value_value__error(self):

        # Arrange
        radius = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Blur(radius=radius)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Blur(1)(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Blur(1)
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()