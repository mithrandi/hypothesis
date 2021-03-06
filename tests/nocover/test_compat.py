# coding=utf-8

# This file is part of Hypothesis (https://github.com/DRMacIver/hypothesis)

# Most of this work is copyright (C) 2013-2015 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# https://github.com/DRMacIver/hypothesis/blob/master/CONTRIBUTING.rst for a
# full list of people who may hold copyright, and consult the git log if you
# need to determine who owns an individual contribution.

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

# END HEADER

from __future__ import division, print_function, absolute_import

import pytest
from hypothesis.internal.compat import hrange, qualname, HAS_SIGNATURE, \
    signature_argspec


def test_small_hrange():
    assert list(hrange(5)) == [0, 1, 2, 3, 4]
    assert list(hrange(3, 5)) == [3, 4]
    assert list(hrange(1, 10, 2)) == [1, 3, 5, 7, 9]


def test_large_hrange():
    n = 1 << 1024
    assert list(hrange(n, n + 5, 2)) == [n, n + 2, n + 4]
    assert list(hrange(n, n)) == []

    with pytest.raises(ValueError):
        hrange(n, n, 0)


class Foo():

    def bar(self):
        pass


def test_qualname():
    assert qualname(Foo.bar) == u'Foo.bar'
    assert qualname(Foo().bar) == u'Foo.bar'
    assert qualname(qualname) == u'qualname'

try:
    from inspect import getargspec
except ImportError:
    getargspec = None


def a(b, c, d):
    pass


def b(c, d, *ar):
    pass


def c(c, d, *ar, **k):
    pass


def d(a1, a2=1, a3=2, a4=None):
    pass

if getargspec is not None and HAS_SIGNATURE:
    @pytest.mark.parametrize('f', [
        a, b, c, d
    ])
    def test_agrees_on_argspec(f):
        real = getargspec(f)
        fake = signature_argspec(f)
        assert tuple(real) == tuple(fake)
        for f in real._fields:
            assert getattr(real, f) == getattr(fake, f)
