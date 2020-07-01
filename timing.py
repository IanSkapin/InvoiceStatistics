"""
exploring possible timing improvements
"""

import timeit
import decimal


def float_to_int(value):
    s = str(value)
    return int(s.replace('.', ''))


def float_to_dec(value):
    return decimal.Decimal(str(value))


def to_dec(value):
    return decimal.Decimal(value)


def check_input(values):
    for idx in range(len(values)):
        a, b = divmod(values[idx], 1)
        if b > 99:
            raise ValueError("Invalid invoice value. 1 cent is the smallest acceptable unit.")
        if not 0 < values[idx] < 200_000_000.00:
            raise ValueError(
                "Invalid invoice value. Please make sure the value is positive and smaller than 20,000,000.00")



# print(timeit.timeit('float_to_int(1.11)', setup="from __main__ import float_to_int", number=1000))
# print(timeit.timeit('float_to_dec(1.11)', setup="from __main__ import float_to_dec", number=1000))
# print(timeit.timeit('to_dec(1.11)', setup="from __main__ import to_dec", number=1000))
# print(timeit.timeit('InvoiceStats.scale_up(1.11)', setup="from invoice_statistics import InvoiceStats", number=1000))
print(timeit.timeit('l = [x/100 for x in range(1, 100)]; InvoiceStats.check_input(l)', setup="from invoice_statistics import InvoiceStats", number=10000))
print(timeit.timeit('l = [x/100 for x in range(1, 100)]; check_input(l)', setup="from __main__ import check_input", number=10000))

