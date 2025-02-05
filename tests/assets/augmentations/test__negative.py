import unittest
from CVAugmentor.assets.augmentations._negative import Negative
from PIL import Image, ImageChops


class TestNegative(unittest.TestCase):

    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Negative()(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Negative()
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()