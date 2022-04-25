import os
import time
from typing import Callable, Tuple

from pytest import fixture


@fixture(scope='function')
def prepare_test_data() -> Callable:
    files = []

    def _prepare_test_data(initial_data_file_path: str) -> Tuple[str, str]:
        test_data_path = os.path.join(os.getcwd(), f'tests/test_data_{str(int(time.time_ns()))}.txt')
        test_result_path = os.path.join(os.getcwd(), f'tests/test_result_{str(int(time.time_ns()))}.txt')
        with open(initial_data_file_path, 'r') as initial_data:
            for item in initial_data:
                test_data, _ = item.split('#')
                with open(test_data_path, 'a') as test_data_file, open(test_result_path, 'a') as test_result_file:
                    test_data_file.write(f'{test_data}\n')
                    test_result_file.write(f'{item.replace("#", " ")}')

            files.append(test_data_path)
            files.append(test_result_path)

        return test_data_path, test_result_path

    yield _prepare_test_data

    for file in files:
        os.remove(file)
