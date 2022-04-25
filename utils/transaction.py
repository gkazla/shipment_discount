from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Union, List

from utils.providers import Provider, Providers

PROVIDERS = Providers.from_json_file(path='providers.json')


@dataclass(frozen=True)
class Transaction:
    """
    Transaction entity of the shipping request.
    """
    shipment_date: Optional[date] = None
    package_size: Optional[str] = None
    provider: Optional[Provider] = None

    @classmethod
    def load(cls, args: List[str]) -> Union[Transaction, None]:
        """
        Creates transaction entity using the given arguments.

        :param args: A list of arguments for creation of the transaction entity.
            e.g. [
                shipment_data,
                pack_size,
                provider
            ]
        :return: Transaction entity if valida arguments were given in other case None.
        """
        try:
            provider = PROVIDERS.get_provider(provider_name=args[2])
            provider.validate_pack_size(args[1].upper())
            return cls(
                shipment_date=datetime.strptime(str(args[0]), '%Y-%m-%d'),
                package_size=args[1].upper(),
                provider=provider
            )
        except (ValueError, IndexError):
            return None
