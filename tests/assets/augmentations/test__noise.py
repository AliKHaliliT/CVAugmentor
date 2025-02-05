import unittest
from CVAugmentor.assets.augmentations._noise import Noise
from PIL import Image, ImageChops


class TestNoise(unittest.TestCase):

    def test_intensity_wrong__value_value__error(self):

        # Arrange
        intensity = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Noise(intensity=intensity)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Noise()(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Noise()
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()