import unittest
from CVAugmentor.assets.utils.sort_alphanumerically import sorted_alphanumerically


class TestSortedAlphanumerically(unittest.TestCase):

    def test_input__list_wrong__value_value__error(self):

        # Arrange
        input_list = None

        # Act and Assert
        with self.assertRaises(ValueError):
            sorted_alphanumerically(input_list=input_list)


    def test_output_input__list_correct__output__list(self):

        # Arrange
        input_list = ["0", "1", "10", "001"]
        correct_output_list = ["0", "1", "001", "10"]
        
        # Act
        output_list = sorted_alphanumerically(input_list=input_list)
            
        # Assert
        self.assertEqual(output_list, correct_output_list)


if __name__ == "__main__":
    unittest.main()