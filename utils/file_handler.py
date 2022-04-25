from typing import Generator


class FileHandler:
    def __init__(self, path: str) -> None:
        self._path = path

    def read(self) -> Generator:
        with open(self._path, 'r') as file:
            for line in file:
                line = line.strip()
                yield line

    def append(self, value: str) -> None:
        with open(self._path, 'a') as file:
            file.write(f'{value}\n')
