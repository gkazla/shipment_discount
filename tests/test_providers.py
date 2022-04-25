import json
import os

from pytest import raises

from utils.providers import Providers


def test_loading_of_providers() -> None:
    json_file = os.path.join(os.getcwd(), 'tests/providers.json')
    with open(json_file, 'r') as file:
        providers_json = json.load(file)

    providers = Providers.from_json_file(json_file)

    for provider in providers_json:
        result = providers.get_provider(provider_name=provider['provider_name'])

        # Check is provider correctly loaded.
        assert result.provider_name == provider['provider_name']

        for package_size in provider['shipment_prices'].keys():
            # Check provider pack sizes.
            assert result.validate_pack_size(package_size) is None
            # Check provider shipment prices.
            assert result.shipment_price(package_size) == provider['shipment_prices'][package_size]

        # Check lowest prices among all providers of all package sizes.
        assert providers.get_lowest_price('S') == 19.99
        assert providers.get_lowest_price('M') == 30
        assert providers.get_lowest_price('L') == 40

        # Check non-existing provider and package size. Expect raise of ValueError.
        with raises(ValueError):
            providers.get_provider(provider_name='FakeProvider')
            result.validate_pack_size('XXL')
