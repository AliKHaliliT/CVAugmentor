import unittest
from CVAugmentor.assets.augmentations._shear import Shear
from PIL import Image, ImageChops


class TestShear(unittest.TestCase):

    def test_shear_wrong__value_value__error(self):

        # Arrange
        shear = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Shear(shear=shear)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Shear()(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Shear()
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()