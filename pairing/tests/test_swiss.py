# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from pairing.utils import Pairing


class TestPairing(object):
    def test_pairing(self):
        '''
        If we have an ordered list 1,2,3,4,5,6
        slide pairing is (1, 4), (2, 5), (3, 6)
        '''
        params = [{'id': 1, 'score': 0}, {'id': 2, 'score': 0}]
        #output, _ = pair(players)
        p = Pairing(params)
        assert p.output == [(1, 2), ]

    def test_pair_multiple(self):
        params = [
            {'id': 1, 'score': 0},
            {'id': 2, 'score': 0},
            {'id': 3, 'score': 0},
            {'id': 4, 'score': 0}
        ]
        #output, _ = pair(params)
        p = Pairing(params)
        assert p.output == [(1, 3), (2, 4)]

    def test_pair_odd(self):
        params = [
            {'id': 1, 'score': 0},
            {'id': 2, 'score': 0},
            {'id': 3, 'score': 0},
            {'id': 4, 'score': 0},
            {'id': 5, 'score': 0},
        ]
        #import pdb;pdb.set_trace()
        p = Pairing(params)
        #output, remainder = pair(params)
        assert p.remainder == [{'id': 5, 'score': 0}]
        assert p.output == [(1, 3), (2, 4)]

    def test_grouping(self):
        params = [
            {'id': 1, 'score': 2},
            {'id': 2, 'score': 2},
            {'id': 3, 'score': 1},
            {'id': 4, 'score': 1},
            {'id': 5, 'score': 0},
            {'id': 6, 'score': 0}
        ]
        #import pdb;pdb.set_trace()
        p = Pairing(params)
        #output, remainder = pair(params)
        assert p.output == [(1, 2), (3, 4), (5, 6)]

    def test_grouping_bottom_heavy(self):
        '''Test that higher score will fall-through
           to be paired with lower scores
        '''
        params = [
            {'id': 1, 'score': 2},
            {'id': 2, 'score': 1},
            {'id': 3, 'score': 1},
            {'id': 4, 'score': 1},
        ]
        #import pdb;pdb.set_trace()
        p = Pairing(params)
        #output, remainder = pair(params)
        assert p.output == [(1, 2), (3, 4)]

    def test_grouping_topheavy(self):
        params = [
            {'id': 1, 'score': 2},
            {'id': 2, 'score': 2},
            {'id': 3, 'score': 2},
            {'id': 4, 'score': 1},
        ]
        p = Pairing(params)
        #output, remainder = pair(params)
        assert p.output == [(1, 2), (3, 4)]

    def test_topheavy_remainder(self):
        params = [
            {'id': 1, 'score': 2},
            {'id': 2, 'score': 2},
            {'id': 3, 'score': 2},
            {'id': 4, 'score': 1},
            {'id': 5, 'score': 1},
        ]
        #import pdb;pdb.set_trace()
        p = Pairing(params)
        #output, remainder = pair(params)
        assert p.output == [(1, 2), (3, 4)]
        assert p.remainder == {'id': 5, 'score': 1}


class TestHavePlayed(object):

    @pytest.fixture
    def params(self):
        return [
            {'id': 1, 'score': 2},
            {'id': 2, 'score': 2},
            {'id': 3, 'score': 2},
            {'id': 4, 'score': 1},
            {'id': 5, 'score': 1},
            {'id': 6, 'score': 0},
            {'id': 7, 'score': 0},
            {'id': 8, 'score': 0},
            {'id': 9, 'score': 0}
        ]

    def test_pairing(self, params):
        p = Pairing(params)
        #output, remainder = pair(params)
        assert p.output == [(1, 2), (3, 4), (5, 6), (7, 8)]
        assert p.remainder == {'id': 9, 'score': 0}

    def test_history(self, params):
        history = [(3, 4), (1, 5), (2, 6)]
        #import pdb;pdb.set_trace()
        p = Pairing(params, history=history)
        assert p.output == [(1, 2), (3, 5), (4, 6), (7, 8)]
        assert p.remainder == {'id': 9, 'score': 0}


class TestSorting(object):

    def test_sort_by_score(self):
        '''Test that players are sorted by score'''
        params = [
            {'id': 1, 'score': 0},
            {'id': 2, 'score': 2},
            {'id': 3, 'score': 4},
            {'id': 4, 'score': 1},
            {'id': 5, 'score': 1},
        ]
        p = Pairing(params)
        assert p.output == [(3, 2), (4, 5)]
        assert p.remainder == {'id': 1, 'score': 0}
