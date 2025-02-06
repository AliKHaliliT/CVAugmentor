import unittest
from CVAugmentor.assets.augmentations._rotate import Rotate
from PIL import Image, ImageChops


class TestRotate(unittest.TestCase):

    def test_angle_wrong__value_value__error(self):

        # Arrange
        angle = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Rotate(angle=angle)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Rotate(1)(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Rotate(1)
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()