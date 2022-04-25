# Discounts

Problem
----------------------------
When something is purchased, it has to be shipped, various shipping options are available. 
Each item, depending on its size gets an appropriate package size assigned to it:

  * S - Small
  * M - Medium 
  * L - Large 

Shipping price depends on package size and a provider. Approved providers with available 
package sizes and shipping prices can be fed via `providers.json` file.

E.g.
```json
[
  {
    "provider_name": "SimoSiuntos",
    "shipment_prices": {
      "S": 1.5,
      "M": 4.9,
      "L": 6.9
    }
  },
  {
    "provider_name": "JonasShipping",
    "shipment_prices": {
      "S": 2,
      "M": 3,
      "L": 4
    }
  }
]
```

Member's transactions are listed in a file 'input.txt', each line containing: date (without hours, in ISO format), 
package size code, and carrier code, separated with whitespace:
```
2015-02-01 S JonasShipping
2015-02-02 S JonasShipping
2015-02-03 L SimoSiuntos
2015-02-05 S SimoSiuntos
2015-02-06 S JonasShipping
2015-02-06 L SimoSiuntos
2015-02-07 L JonasShipping
2015-02-08 M JonasShipping
2015-02-09 L SimoSiuntos
2015-02-10 L SimoSiuntos
2015-02-10 S JonasShipping
2015-02-10 S JonasShipping
2015-02-11 L SimoSiuntos
2015-02-12 M JonasShipping
2015-02-13 M SimoSiuntos
2015-02-15 S JonasShipping
2015-02-17 L SimoSiuntos
2015-02-17 S JonasShipping
2015-02-24 L SimoSiuntos
2015-02-29 CUSPS
2015-03-01 S JonasShipping
```

Discount rules:
* All S shipments should always match the lowest S package price among the providers.
* The third L shipment via SimoSiuntos should be free, but only once a calendar month.
* Accumulated discounts cannot exceed 10 € in a calendar month. If there are not enough funds to fully
cover a discount this calendar month, it should be covered partially.



Usage
--------------------------------------

To run solution in the terminal enter command: 
```
make
```

To run tests enter command:
```
pytest
```


