import os
import random
import unittest

import requests


response_code = int


class BaseTest(unittest.TestCase):
    _base_url = os.environ["BASE_URL"]

    def calculate(
        self, user_id: int, x_data_type: str, y_data_type: str,
        x: list[tuple[str, float]], y: list[tuple[str, float]]
    ) -> response_code:
        """
        Call `calculate` method and return response_code
        """

        json_data = {
            "user_id": user_id,
            "data": {
                "x_data_type": x_data_type,
                "y_data_type": y_data_type,
                "x": [
                    {"date": date, "value": value}
                    for date, value in x
                ],
                "y": [
                    {"date": date, "value": value}
                    for date, value in y
                ],
            }
        }
        return requests.post(
            f"{self._base_url}/calculate", json=json_data
        ).status_code

    def correlation(
        self, user_id: int, x_data_type: str, y_data_type: str
    ) -> tuple[response_code, tuple[float, float] | None]:
        """
        Call `correlation` method and return
        tuple(response_code, correlation),
        where correlation is tuple (value, p_value) if response_code == 200
        else None
        """

        response = requests.get(
            f"{self._base_url}/correlation",
            params={
                "user_id": user_id,
                "x_data_type": x_data_type,
                "y_data_type": y_data_type
            }
        )
        if response.status_code != 200:
            return (response.status_code, None)

        correlation = response.json()["correlation"]
        return (200, (correlation["value"], correlation["p_value"]))

    def generate_random_date(self) -> str:
        """
        Dummy date generator
        """

        year = random.randint(1950, 2050)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month}-{day}"

    def generate_random_value(
        self, min_border: float = -100, max_border: float = 100
    ) -> float:
        """
        Dummy random value generator
        """

        return random.uniform(min_border, max_border)

    def generate_random_user_ids(
        self, n: int, begin: int = -1000, end: int = 1000
    ) -> list[int]:
        """
        Generates list of `n` unique integers
        from uniform distribution [begin; end]
        """

        ids_set = set()
        while len(ids_set) < n:
            value = random.randint(begin, end)
            ids_set.add(value)
        return list(ids_set)

    def generate_letter_sequence(
        self, letter_begin: str, letter_end: str
    ) -> list[str]:
        """
        Returns sequence of letters
        for example, generate_letter_sequence("a", "c") == ["a", "b", "c"]
        """

        return [
            chr(i)
            for i in range(ord(letter_begin), ord(letter_end) + 1)
        ]

    def generate_random_type_names(
        self, n: int, begin_length: int = 1, end_length: int = 20
    ) -> list[str]:
        symbols = self.generate_letter_sequence("a", "z") +\
            self.generate_letter_sequence("A", "Z") +\
            self.generate_letter_sequence("а", "я") +\
            self.generate_letter_sequence("А", "Я") +\
            self.generate_letter_sequence("0", "9")

        name_set = set()
        while len(name_set) < n:
            cur_length = random.randint(begin_length, end_length)
            cur_name = "".join(
                [random.choice(symbols) for _ in range(cur_length)]
            )
            name_set.add(cur_name)

        return list(name_set)

    def generate_random_date_values(
        self, n: int, n_additional: int
    ) -> tuple[list[tuple[str, float]], list[tuple[str, float]]]:
        """
        Generate two lists in format [(date, value), ...]:
            first list has length `n`,
            second list has length `n + n_additional`,
            second list has `n` values from the first list
                and `n_additional` values not from the first list
        """

        base_dates = [
            self.generate_random_date() for _ in range(n)
        ]

        base_set = set(base_dates)
        additional_dates = []
        while len(additional_dates) < n_additional:
            cur_date = self.generate_random_date()
            if cur_date not in base_set:
                additional_dates.append(cur_date)

        first_values = [
            self.generate_random_value() for _ in range(n)
        ]
        second_values = [
            self.generate_random_value() for _ in range(n + n_additional)
        ]

        first_date_values = list(zip(base_dates, first_values))
        second_date_values = list(zip(
            base_dates + additional_dates,
            second_values
        ))

        return first_date_values, second_date_values
