import unittest
from CVAugmentor.assets.augmentations._no_augmentation import NoAugmentation
from PIL import Image, ImageChops


class TestNoAugmentation(unittest.TestCase):

    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            NoAugmentation()(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = NoAugmentation()
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertFalse(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()