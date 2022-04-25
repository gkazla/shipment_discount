from typing import Callable

from main import process
from utils.file_handler import FileHandler


def test_shipment_discounts(prepare_test_data: Callable) -> None:
    inputs, results = prepare_test_data('tests/data.txt')

    results = FileHandler(path=results).read()

    for response in process(inputs):
        result = next(results)
        assert response == result, result
