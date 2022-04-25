from typing import Callable, List, Optional

from utils.transaction import Transaction, PROVIDERS

MAX_MONTHLY_DISCOUNT = 10.00


class Discount:
    def __init__(self):
        self._amount: float = MAX_MONTHLY_DISCOUNT
        self._occurrence: int = 0
        self._transaction: Optional[Transaction] = None

    @property
    def discounts(self) -> List[Callable]:
        """
        Make a list of available discount calculation methods.

        :return: A list of available discounts calculation methods.
        """
        return [
            self._small_package_discount,
            self._large_package_discount,
        ]

    def get(self, transaction: Transaction) -> float:
        """
        Retrieve an available discount for the given shipping transaction.

        :param transaction: Transaction entity of the shipping request.
        :return: Discount amount.
        """
        discount = 0
        self._transaction = transaction
        for discount_ in self.discounts:
            if discount := discount_():
                break

        return discount

    def reset(self) -> None:
        """
        Reset of the discount parameters.

        :return: No return.
        """
        self._amount = MAX_MONTHLY_DISCOUNT
        self._occurrence = 0

    def _small_package_discount(self) -> float:
        """
        All small (S) shipments should always match the lowest shipping price among the providers.

        :return: Discount amount.
        """
        discount = 0
        if self._transaction.package_size == 'S':
            standard_price = self._transaction.provider.shipment_price(self._transaction.package_size)
            lowest_price = PROVIDERS.get_lowest_price(pack_size=self._transaction.package_size)
            discount = standard_price - lowest_price

        return self._month_discount_amount(discount)

    def _large_package_discount(self) -> float:
        """
        The third L shipment via SimoSiuntos should be free, but only once a calendar month.

        :return: Discount amount.
        """
        discount = 0
        if self._transaction.package_size == 'L' and self._transaction.provider.provider_name == 'SimoSiuntos':
            self._occurrence += 1

            if self._occurrence == 3:
                discount = self._transaction.provider.shipment_price(self._transaction.package_size)

        return self._month_discount_amount(discount)

    def _month_discount_amount(self, desired_discount_amount: float) -> float:
        """
        Accumulated discounts cannot exceed MAX MONTHLY DISCOUNT in a calendar month.
        If there are not enough funds left, give partially discount.

        :param desired_discount_amount: Discount amount to inspect.
        :return: Discount amount.
        """
        if self._amount < desired_discount_amount:
            desired_discount_amount, self._amount = self._amount, 0
        else:
            self._amount = round(self._amount - desired_discount_amount, 2)

        return desired_discount_amount
