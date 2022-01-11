from itertools import product
import unittest

from base import BaseTest


class TestPearson(BaseTest):
    """
    Test to check whether Pearson properties satisfied
    """

    def get_correlation(
        self, user_id: int, x_data_type: str, y_data_type: str,
        x: list[tuple[str, float]], y: list[tuple[str, float]]
    ) -> tuple[float, float]:
        """
        Get result of method sequence `calculate` + `correlation`
        """

        self.calculate(user_id, x_data_type, y_data_type, x, y)
        _, (value, p_value) = self.correlation(
            user_id, x_data_type, y_data_type
        )
        return value, p_value

    def test_range(self):
        """
        Test whether Pearson'r is in range [-1; 1]
        """

        user_id = 0
        x_data_type = "X"
        y_data_type = "Y"
        for _ in range(20):
            data1, data2 = self.generate_random_date_values(70, 30)
            value, _ = self.get_correlation(
                user_id, x_data_type, y_data_type, data1, data2
            )
            self.assertTrue(-1 <= value <= 1)

    def check_permutation_properties(
        self, user_ids: list[int], type_names: list[str],
        data1: list[tuple[str, float]], data2: list[tuple[str, float]]
    ):
        """
        Check that `calculate` + `correlation` gives same result for:
            1. same data and permuted type names
            2. same type names and permuted data
        """
        for user_id, (type1, type2) in product(
            user_ids, product(type_names, type_names)
        ):
            value_pt1, p_value_pt1 = self.get_correlation(
                user_id, type1, type2, data1, data2
            )
            value_pt2, p_value_pt2 = self.get_correlation(
                user_id, type2, type1, data1, data2
            )

            self.assertEqual(
                value_pt1, value_pt2, "equal_values_permute_types"
            )
            self.assertEqual(
                p_value_pt1, p_value_pt2, "equal_p_values_permute_types"
            )

            value_pv1, p_value_pv1 = self.get_correlation(
                user_id, type1, type2, data1, data2
            )
            value_pv2, p_value_pv2 = self.get_correlation(
                user_id, type1, type2, data2, data1
            )

            self.assertEqual(
                value_pv1, value_pv2, "equal_values_permute_values"
            )
            self.assertEqual(
                p_value_pv1, p_value_pv2, "equal_p_values_permute_values"
            )

    def test_permute_data_predefined(self):
        """
        Test `calculate` + `correlation` gives same result for:
            1. same data and permuted type names
            2. same type names and permuted data
        on predefined data
        """

        data1 = [
            ("2021-06-01", 0.2), ("2021-06-03", 6.4), ("2021-06-06", 10)
        ]
        data2 = [
            ("2021-06-01", 0.4), ("2021-06-03", -5.2),
            ("2021-06-06", -7), ("2021-06-10", 2)
        ]
        ids = [5, 7, 2, 501, 5192]
        type_names = ["r1", "asdjiqds", "1283u", "san  asdokna"]

        self.check_permutation_properties(ids, type_names, data1, data2)

    def test_permute_data_random(self):
        """
        Test `calculate` + `correlation` gives same result for:
            1. same data and permuted type names
            2. same type names and permuted data
        on random data
        """

        ids = self.generate_random_user_ids(5)
        data1, data2 = self.generate_random_date_values(10, 5)
        type_names = self.generate_random_type_names(6)

        self.check_permutation_properties(ids, type_names, data1, data2)

    def check_max_correlated(
        self, user_ids: list[int], type_names: list[str],
        data: list[tuple[str, float]]
    ):
        """
        Check that `calculate` + `correlation` gives -1 and 1
        on the same data
        """
        inversed_data = [(d, -v) for d, v in data]

        for user_id, (type1, type2) in product(
            user_ids, product(type_names, type_names)
        ):
            value, _ = self.get_correlation(
                user_id, type1, type2, data, data
            )
            self.assertEqual(
                value, 1, "data is maximally correlated with itself"
            )

            inv_value, _ = self.get_correlation(
                user_id, type1, type2, data, inversed_data
            )
            self.assertEqual(
                inv_value, -1,
                "data is maximally negatively correlated with itself"
            )

    def test_max_correlated_predefined(self):
        """
        Test `calculate` + `correlation` gives maximal result
        on predefined data
        """

        data = [
            ("2021-06-01", 0.2), ("2021-06-03", 6.4), ("2021-06-06", 10)
        ]
        ids = [5, 7, 2, 501, 5192]
        type_names = ["r1", "asdjiqds", "1283u", "san  asdokna"]

        self.check_max_correlated(ids, type_names, data)

    def test_max_correlated_random(self):
        """
        Test `calculate` + `correlation` gives maximal result
        on random data
        """

        data, _ = self.generate_random_date_values(50, 0)
        ids = self.generate_random_user_ids(5)
        type_names = self.generate_random_type_names(5)

        self.check_max_correlated(ids, type_names, data)


if __name__ == '__main__':
    unittest.main()
