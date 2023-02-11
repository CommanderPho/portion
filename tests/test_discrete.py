import pytest

import portion as P


class IntInterval(P.AbstractDiscreteInterval):
    step = 1


D = P.create_api(IntInterval)


class TestCreateAPI:
    def test_type(self):
        assert D.Interval == IntInterval

    def test_helper_types(self):
        assert isinstance(D.closed(0, 1), IntInterval)
        assert isinstance(D.open(0, 1), IntInterval)
        assert isinstance(D.closedopen(0, 1), IntInterval)
        assert isinstance(D.openclosed(0, 1), IntInterval)
        assert isinstance(D.singleton(0), IntInterval)
        assert isinstance(D.empty(), IntInterval)

    def test_io(self):
        assert isinstance(D.from_string('[1, 2]', conv=int), IntInterval)
        assert D.from_string('[1, 2]', conv=int) == D.closed(1, 2)

        assert isinstance(D.from_data([(D.CLOSED, 1, 2, D.OPEN)]), IntInterval)
        assert D.from_data([(D.CLOSED, 1, 2, D.OPEN)]) == D.closedopen(1, 2)

    def test_dict_type(self):
        assert D.IntervalDict.__name__ != 'IntervalDict'
        assert D.IntervalDict._klass == IntInterval
        assert isinstance(D.IntervalDict().domain(), IntInterval)


class TestIntInterval:
    def test_empty_and_singletons(self):
        assert D.open(1, 2).empty
        assert D.closed(1, 1) == D.singleton(1)
        assert D.open(0, 2) == D.singleton(1)
        assert D.openclosed(1, 2) == D.singleton(2)
        assert D.closedopen(1, 2) == D.singleton(1)

    def test_merge(self):
        assert D.singleton(1) | D.singleton(2) == D.closed(1, 2)
        assert D.closed(0, 1) | D.closed(2, 3) == D.closed(0, 3)

        assert D.openclosed(0, 2) | D.closedopen(3, 5) == D.open(0, 5) == D.closed(1, 4)
        assert not (D.closedopen(0, 1) | D.openclosed(1, 2)).atomic

    def test_adjacent(self):
        assert D.singleton(1).adjacent(D.singleton(2))
        assert not D.singleton(1).adjacent(D.singleton(3))


