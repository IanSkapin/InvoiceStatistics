import mock
import pytest
from .. import invoice_statistics


class TestInvoiceStats:

    @pytest.mark.parametrize('value', [0.001, 0.999, 1e-64])
    def test_check_input_cents(self, value):
        with pytest.raises(ValueError):
            invoice_statistics.InvoiceStats.check_input([value])

    @pytest.mark.parametrize('value', [0, 200_000_000.00])
    def test_check_input_out_of_bounds(self, value):
        with pytest.raises(ValueError):
            invoice_statistics.InvoiceStats.check_input([value])

    @pytest.mark.parametrize('value, out', [
        (0.01, 1),
        (0.99, 99),
        (0.005, 0),
        (0.0051, 1),
    ])
    def test_scale_up(self, value, out):
        assert invoice_statistics.InvoiceStats.scale_up(value) == out

    @pytest.mark.parametrize('mean, mean_weight, values_sum, new_mean, new_weight', [
        (25.5, 50, 3675, 50, 99),
        (99.99, 1, 100, 99.995, 2),
        (99.99, 1, 3*100, 99.9975, 4),
        (99.99, 1, 4*100, 99.998, 5),
        (99.99, 1, 7*100, 99.99875, 8),
        (99.99, 1, 19*100, 99.9995, 20),
        (99.99, 1, 100.01, 100, 2),
    ])
    def test_update_mean(self, mean, mean_weight, values_sum, new_mean, new_weight):
        istat = invoice_statistics.InvoiceStats()
        istat.mean = mean
        istat.mean_weight = mean_weight
        istat._update_mean(values_sum, new_weight - mean_weight)
        assert istat.mean == new_mean
        assert istat.mean_weight == new_weight

    def test_add_invoice(self):
        istat = invoice_statistics.InvoiceStats()
        with mock.patch.object(istat, 'check_input') as mock_check,\
                mock.patch.object(istat, 'scale_up', return_value=456) as mock_scale, \
                mock.patch.object(istat, 'insert') as mock_insert, \
                mock.patch.object(istat, '_update_mean') as mock_update:
            istat.add_invoice(123)
            mock_check.assert_called_once_with([123])
            mock_scale.assert_called_once_with(123)
            mock_insert.assert_called_once_with(456)
            mock_update.assert_called_once_with(456, 1)

    def test_add_invoices(self):
        istat = invoice_statistics.InvoiceStats()
        with mock.patch.object(istat, 'check_input') as mock_check,\
                mock.patch.object(istat, 'scale_up', return_value=1) as mock_scale, \
                mock.patch.object(istat, 'insert_list') as mock_insert, \
                mock.patch.object(istat, '_update_mean') as mock_update:
            l = [123, 456]
            istat.add_invoices(l)
            mock_check.assert_called_once_with(l)
            mock_scale.has_calls([mock.call(x) for x in l])
            mock_insert.assert_called_once()
            mock_update.assert_called_once()

    def test_clear(self):
        with mock.patch.object(invoice_statistics.FastMedian, 'clear') as mock_clear:
            istat = invoice_statistics.InvoiceStats()
            istat.mean = 123
            istat.mean_weight = 123
            istat.clear()
            assert istat.mean == 0
            assert istat.mean_weight == 0
            mock_clear.assert_called_once()

    @pytest.mark.parametrize('median, out', [
        (100, 1),
        (101, 1.01),
        (1, 0.01),
        (199, 1.99),
        (99, 0.99),
    ])
    def test_get_median(self, median, out):
        istat = invoice_statistics.InvoiceStats()
        istat.max_pq = True
        with mock.patch.object(istat, 'median', return_value=median) as mock_median:
            assert istat.get_median() == out
            mock_median.assert_called_once()

    def test_get_median_none(self):
        istat = invoice_statistics.InvoiceStats()
        assert istat.get_median() == None


    @pytest.mark.parametrize('value, rounded', [
        (1, 0.01),
        (1005, 10.05),
        (0, None),
    ])
    def test_get_mean(self, value, rounded):
        istats = invoice_statistics.InvoiceStats()
        istats.mean = value
        assert istats.get_mean() == rounded



