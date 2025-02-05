import unittest
from CVAugmentor.assets.augmentations._flip import Flip
from PIL import Image, ImageChops


class TestFlip(unittest.TestCase):

    def test_flip__type_wrong__value_value__error(self):

        # Arrange
        flip_type = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Flip(flip_type=flip_type)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Flip()(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Flip()
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()