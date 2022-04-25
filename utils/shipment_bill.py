from typing import Union

from utils.discount import Discount
from utils.transaction import Transaction


class ShipmentBill:
    def __init__(self) -> None:
        self._month: Union[int, None] = None
        self._discount: Discount = Discount()

    def make(self, input_: str) -> str:
        """
        Prepares package shipping bill using given transaction string.

        :param input_: String representation of transaction in a format:
            YYYY-mm-dd package_size provider
            e.g.: 2022-04-25 L DHLExpress
        :return: String representation of package shipping bill.
        """
        if transaction := Transaction.load(input_.split()):
            if self._month != transaction.shipment_date.month:
                self._month = transaction.shipment_date.month
                self._discount.reset()

            discount_amount = self._discount.get(transaction=transaction)

            standard_shipment_price = transaction.provider.shipment_prices[transaction.package_size]
            discounted_price = standard_shipment_price - discount_amount

            discounted_price = self.to_string(discounted_price)
            discount_amount = self.to_string(discount_amount)

            return f'{input_} {discounted_price} {discount_amount}'
        else:
            return f'{input_} Ignored'

    @staticmethod
    def to_string(value: float) -> str:
        """
        Converts given value to a string keeping two decimal places format.
        If value is 0 (zero) returns - (minus) character.

        :param value:
        :return: Return nicely formatted string of given float value.
        """
        if not value:
            return '-'

        return format(value, '.2f')
