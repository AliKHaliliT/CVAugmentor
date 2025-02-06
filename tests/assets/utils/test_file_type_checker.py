import unittest
from CVAugmentor.assets.utils.file_type_checker import is_target_type


class TestIsTargetType(unittest.TestCase):

    def test_filename_wrong__value_value__error(self):

        # Arrange
        filename = None

        # Act and Assert
        with self.assertRaises(ValueError):
            is_target_type(filename=filename, target="image")

    
    def test_target_wrong__value_value__error(self):

        # Arrange
        target = None

        # Act and Assert
        with self.assertRaises(ValueError):
            is_target_type(filename="filename.jpg", target=target)


    def test_output_input__parameters_correct__boolean(self):

        # Arrange
        filename = "filename.jpg"
        target = "image"
        
        # Act
        target_type = is_target_type(filename=filename, target=target)
            
        # Assert
        self.assertEqual(target_type, True)


if __name__ == "__main__":
    unittest.main()