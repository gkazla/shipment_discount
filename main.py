import os
import time
from typing import Generator

from utils.file_handler import FileHandler
from utils.shipment_bill import ShipmentBill


def process(path: str) -> Generator:
    inputs = FileHandler(path).read()
    shipment_bill = ShipmentBill()

    for input_ in inputs:
        yield shipment_bill.make(input_)


if __name__ == '__main__':
    output = FileHandler(path=os.path.join(os.getcwd(), f'outputs_{str(int(time.time_ns()))}.txt'))

    for response in process(path=os.path.join(os.getcwd(), 'input.txt')):
        output.append(response)
