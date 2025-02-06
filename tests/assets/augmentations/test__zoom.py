import unittest
from CVAugmentor.assets.augmentations._zoom import Zoom
from PIL import Image, ImageChops


class TestZoom(unittest.TestCase):

    def test_zoom__size_wrong__value_value__error(self):

        # Arrange
        zoom_size = "-1"

        # Act and Assert
        with self.assertRaises(ValueError):
            Zoom(zoom_size=zoom_size)


    def test_image_wrong__type_type__error(self):

        # Arrange
        image = "-1"

        # Act and Assert
        with self.assertRaises(TypeError):
            Zoom((10, 10))(image)


    def test_output_image_augmented__image(self):

        # Arrange
        augmentor = Zoom((10, 10))
        image = Image.new("RGB", (64, 32))

        # Act
        augmneted_image = augmentor(image)

        # Assert
        self.assertIsNotNone(bool(ImageChops.difference(augmneted_image, image).getbbox()))


if __name__ == "__main__":
    unittest.main()