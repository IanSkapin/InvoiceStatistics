import mock
import pytest
from _collections_abc import Iterable

from .. import median


def test_maxq_heappush():
    l = 5*[0]
    with mock.patch.object(median.minq, '_siftdown_max') as mock_sift:
        median.maxq.heappush(l, 0)
        mock_sift.assert_called_once_with(l, 0, 5)


class TestFastMedian:
    @pytest.mark.parametrize('array', [None, [1]])
    def test_init(self, array):
        with mock.patch.object(median.FastMedian, '_push') as mock_push, \
                mock.patch.object(median.FastMedian, '_balance') as mock_balance:
            fm = median.FastMedian(array)
            assert fm.min_pq == []
            assert fm.max_pq == []
            if array:
                mock_balance.assert_called_once()
                assert mock_push.call_count == len(array)

    def test_elements(self):
        fm = median.FastMedian(range(10))
        elements = fm.elements()
        assert isinstance(elements, Iterable)
        assert set(elements) == set(range(10))

    @pytest.mark.parametrize('min, max, out', [
        ([50, 52], [45, 32], 47.5),
        ([50, 52], [45], 50),
        ([50, 52], [49.99, 32], 50),
        ([50, 52], [49.97, 32], 49.98),
    ])
    def test_median(self, min, max, out):
        fm = median.FastMedian()
        fm.min_pq = min
        fm.max_pq = max
        assert fm.median() == out

    @pytest.mark.parametrize('items, out', [
        (range(100), 4950),
    ])
    def test_insert_list(self, items, out):
        fm = median.FastMedian()
        with mock.patch.object(fm, '_push') as mock_push, \
                mock.patch.object(fm, '_balance') as mock_balance:
            assert fm.insert_list(items) == out
            mock_push.has_calls([mock.call(x) for x in items])
            mock_balance.assert_called_once()

    def test_insert(self):
        fm = median.FastMedian()
        with mock.patch.object(fm, '_push') as mock_push,\
                mock.patch.object(fm, '_balance') as mock_balance:
            fm.insert('qwe')
            mock_push.assert_called_once_with('qwe')
            mock_balance.assert_called_once()

    @pytest.mark.parametrize('min_pq, item', [
        ([], 0),
        ([0], 1),
    ])
    def test_push_min(self, min_pq, item):
        with mock.patch.object(median.minq, 'heappush') as mock_min,\
                mock.patch.object(median.maxq, 'heappush') as mock_max:
            fm = median.FastMedian()
            fm.min_pq = min_pq
            fm._push(item)
            mock_min.assert_called_once_with(fm.min_pq, item)
            mock_max.assert_not_called()

    def test_push_max(self):
        with mock.patch.object(median.minq, 'heappush') as mock_min, \
                mock.patch.object(median.maxq, 'heappush') as mock_max:
            fm = median.FastMedian()
            fm.min_pq = [1]
            fm._push(0)
            mock_max.assert_called_once_with(fm.max_pq, 0)
            mock_min.assert_not_called()

    def test_clear(self):
        fm = median.FastMedian([1, 2, 3])
        fm.clear()
        assert fm.min_pq == []
        assert fm.max_pq == []

    @pytest.mark.parametrize('i_min, i_max, o_min, o_max', [
        ([], [], [], []),
        ([], [2, 1], [], [2, 1]),  # not a valid initial state
        ([5, 10, 15], [], [10, 15], [5]),
        ([5, 10, 15, 20], [], [15, 20], [10, 5]),
        ([10], [9, 9, 9, 9], [9, 10, 9], [9, 9]),
    ])
    def test_balance(self, i_min, i_max, o_min, o_max):
        fm = median.FastMedian()
        fm.min_pq = i_min
        fm.max_pq = i_max
        fm._balance()
        assert fm.min_pq == o_min
        assert fm.max_pq == o_max