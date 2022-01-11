from itertools import product
import unittest

from base import BaseTest


class TestRequests(BaseTest):
    """
    Test to check whether API calls successful
    (checks success codes)
    """

    def check_calculate_request(
        self, user_id: int, x_data_type: str, y_data_type: str,
        x: list[tuple[str, float]], y: list[tuple[str, float]]
    ):
        response_code = self.calculate(
            user_id, x_data_type, y_data_type, x, y
        )
        self.assertEqual(response_code, 200)

    def test_calculate_predefined(self):
        """
        Test `calculate` for success on predefined values
        """

        data = [("2021-06-01", 0.2), ("2021-06-03", 6.4), ("2021-06-06", -5)]
        ids = [5, 7, 2, 501, 5192]
        type_names = ["r1", "asdjiqds", "1283u", "san  asdokna"]

        for user_id, type_name in product(ids, type_names):
            self.check_calculate_request(
                user_id, type_name, type_name, data, data
            )

    def test_calculate_random(self):
        """
        Test `calculate` for success on random values
        """
        user_ids = self.generate_random_user_ids(5)
        data1, data2 = self.generate_random_date_values(100, 30)
        type_names = self.generate_random_type_names(10)

        for user_id, (type1, type2) in product(
            user_ids, product(type_names, type_names)
        ):
            self.check_calculate_request(
                user_id, type1, type2, data1, data2
            )

    def check_correlation_request(
        self, user_id: int, x_data_type: str, y_data_type: str,
        x: list[tuple[str, float]], y: list[tuple[str, float]]
    ):
        response_code_calculate = self.calculate(
            user_id, x_data_type, y_data_type, x, y
        )
        self.assertEqual(
            response_code_calculate, 200, "successful_calculate"
        )

        response_code_correlation, correlation = self.correlation(
            user_id, x_data_type, y_data_type
        )
        self.assertEqual(
            response_code_correlation, 200, "successful_correlation"
        )
        self.assertTrue(
            isinstance(correlation, tuple), "correlation_is_tuple"
        )
        self.assertTrue(
            len(correlation) == 2, "correlation_float_tuple"
        )

    def test_correlation_predefined(self):
        """
        Test `calculate` + `correlation` for success on predefined data
        """

        data = [("2021-06-01", 0.2), ("2021-06-03", 6.4), ("2021-06-06", -5)]
        ids = [5, 7, 2, 501, 5192]
        type_names = ["r1", "asdjiqds", "1283u", "san  asdokna"]

        for user_id, type1, type2 in product(ids, type_names, type_names):
            self.check_correlation_request(
                user_id, type1, type2, data, data
            )

    def test_correlation_random(self):
        """
        Test `calculate` + `correlation` for success on random data
        """

        user_ids = self.generate_random_user_ids(5)
        data1, data2 = self.generate_random_date_values(100, 30)
        type_names = self.generate_random_type_names(10)

        for user_id, (type1, type2) in product(
            user_ids, product(type_names, type_names)
        ):
            self.check_correlation_request(
                user_id, type1, type2, data1, data2
            )

    def test_short_calculate_predefined(self):
        """
        Test `calculate` + `correlation` for unsuccess on short dates
        """

        ids = [5, 7, 2, 501, 5192]
        type_names = ["r1", "asdjiqds", "1283u", "san  asdokna"]
        data1 = [("2021-06-01", 0.2), ("2021-06-03", 6.4)]
        data2 = [("2021-06-01", 0.2), ("2021-06-04", 6.4)]

        for user_id, (type1, type2) in product(
            ids, product(type_names, type_names)
        ):
            response_code_calculate = self.calculate(
                user_id, type1, type2, data1, data2
            )
            self.assertNotEqual(
                response_code_calculate, 200, "unsuccessful_calculate"
            )

    def test_short_calculate_random(self):
        """
        Test `calculate` + `correlation` for unsuccess on short dates
        """

        user_id = 0
        type_names = self.generate_random_type_names(5)
        data1, data2 = self.generate_random_date_values(1, 1)

        for type1, type2 in product(type_names, type_names):
            response_code_calculate = self.calculate(
                user_id, type1, type2, data1, data2
            )
            self.assertNotEqual(
                response_code_calculate, 200, "unsuccessful_calculate"
            )

    def test_unknown_correlation(self):
        user_id = 0
        unseen_type_names = [
            "hello.world.oh___so_many_dots", "___asdsa___",
            "..ad.as.d..sd.a.s."
        ]
        for type1, type2 in product(unseen_type_names, unseen_type_names):
            response_code_correlation, _ = self.correlation(
                user_id, type1, type2
            )
            self.assertEqual(
                response_code_correlation, 404, f"unknown_correlation, {_}"
            )

if __name__ == '__main__':
    unittest.main()
