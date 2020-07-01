"""
possible worst case scenario and some use cases
"""

import random
from time import time

from invoice_statistics import InvoiceStats


def get_values(cnt):
    return [random.randint(1, 19_999_999_999)/100 for x in range(cnt)]


def report(time, comment):
    print("{}s spent on {}".format(time, comment))


IS = InvoiceStats()
data = get_values(1_000_000)

s = time()
IS.add_invoices(data)
report(time() - s, 'adding 1M invoices')

s = time()
median = IS.get_median()
report(time() - s, 'retrieving the median: {}'.format(median))

s = time()
mean = IS.get_mean()
report(time() - s, 'retrieving the mean: {}'.format(mean))

data = get_values(1_000_000)
s = time()
IS.add_invoices(data)
report(time() - s, 'adding 1M invoices to the 1M invoices')

s = time()
median = IS.get_median()
report(time() - s, 'retrieving the median: {}'.format(median))

s = time()
mean = IS.get_mean()
report(time() - s, 'retrieving the mean: {}'.format(mean))


s = time()
IS.add_invoice(50_000.5)
report(time() - s, 'adding 1 invoice to the 2M invoices')

s = time()
median = IS.get_median()
report(time() - s, 'retrieving the median: {}'.format(median))

s = time()
mean = IS.get_mean()
report(time() - s, 'retrieving the mean: {}'.format(mean))

data = get_values(1_000)
s = time()
IS.add_invoices(data)
report(time() - s, 'adding 1000 invoices to the 2M and 1 invoices')

s = time()
median = IS.get_median()
report(time() - s, 'retrieving the median: {}'.format(median))

s = time()
mean = IS.get_mean()
report(time() - s, 'retrieving the mean: {}'.format(mean))

data = get_values(18_000_000)
s = time()
IS.add_invoices(data)
report(time() - s, 'adding 18M invoices to the 2M and 1001 invoices')

s = time()
median = IS.get_median()
report(time() - s, 'retrieving the median: {}'.format(median))

s = time()
mean = IS.get_mean()
report(time() - s, 'retrieving the mean: {}'.format(mean))


s = time()
IS.clear()
report(time() - s, 'clearing data')

data = list(map(lambda x: x/100, range(1, 200_000_000, 10)))
s = time()
IS.add_invoices(data)
report(time() - s, 'adding 20M invoices in ascending order (possibly worst case scenario)')


s = time()
median = IS.get_median()
report(time() - s, 'retrieving the median: {}'.format(median))

s = time()
mean = IS.get_mean()
report(time() - s, 'retrieving the mean: {}'.format(mean))
