from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class Provider:
    """
    Definition of Provider entity.
    """
    provider_name: str
    shipment_prices: Dict[str, float]

    def validate_pack_size(self, pack_size: str) -> None:
        """
        Validate given package size.

        :param pack_size: String representation of package size. E.g. S or M or L etc.
        :return: No return.
        :raise ValueError: If given package size is not supported by the provider.
        """
        if pack_size not in self.shipment_prices:
            raise ValueError('Invalid package size supplied.')

    def shipment_price(self, pack_size: str) -> float:
        """
        Retrieve shipment price of the given package size.

        :param pack_size: String representation of shipment package size.
        :return: Price of the shipment.
        """
        return self.shipment_prices[pack_size]

    @classmethod
    def from_dict(cls, metadata: Dict[str, Any]) -> Provider:
        """
        Initialize Provider entity using the given Provider metadata.

        :param metadata: Dictionary formatted provider metadata.
        :return: Provider entity.
        """
        return cls(**metadata)


class Providers:
    def __init__(self, providers: List[Provider]) -> None:
        self._providers: List[Provider] = providers

    @property
    def providers(self) -> List[Provider]:
        return self._providers

    def get_provider(self, provider_name: str) -> Provider:
        """
        Retrieve provider by the given provider name from the pool of preloaded providers.

        :param provider_name: A name of the provider.
        :return: Provider entity.
        :raise ValueError: If provider does not exist.
        """
        try:
            return next(
                (provider_ for provider_ in self.providers if provider_.provider_name.lower() == provider_name.lower())
            )
        except StopIteration:
            raise ValueError('Invalid provider supplied.')

    def get_lowest_price(self, pack_size: str) -> float:
        """
        Retrieve the lowest package shipping price among all provides.

        :param pack_size: String representation of shipment package size.
        :return: Lowest shipping price.
        """
        return float(min([provider.shipment_prices[pack_size] for provider in self.providers]))

    @classmethod
    def from_json_file(cls, path: str) -> Providers:
        """
        Initialize Providers entity from the given JSON file.

        File format:
            {
                'provider_name': 'DHL',
                'shipment_prices' : {
                    'S': 10,
                    'M': 20,
                    'L': 30
                }
            }


        :param path: Path of the Providers JSON file.
        :return: Providers entity.
        """
        with open(path, 'r') as file:
            providers = json.load(file)

        providers_list = []
        for provider in providers:
            providers_list.append(Provider.from_dict(provider))

        return cls(providers=providers_list)
