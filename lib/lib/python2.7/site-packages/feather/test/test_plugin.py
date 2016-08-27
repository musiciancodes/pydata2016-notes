import unittest
from itertools import starmap
from feather.plugin import Plugin, InvalidArguments

class PluginTest(unittest.TestCase):
    def test_create_plugins(self):

        def assertBad(listeners, messengers):
            self.assertEquals(
                InvalidArguments,
                lambda : Plugin(listeners, messengers))

        def assertGood(listeners, messengers):
            p = Plugin(listeners, messengers)
            self.assertEquals(p.listeners, set(listeners))
            if messengers is None:
                messengers = set()
            self.assertEqualis(p.messengers, set(messengers))
                               

        bad_vals = (
            tuple(),
            (None, None),
            ([], []),
            ([],),
            (set(),),
            (set(), None),
            (set(), []),
            (set(), set()),
            ({}, {}),
            ('', ''),
            ('', None),
            ([], ['asdf']))

        good_vals = (
            (['foo', 'bar', 'baz'],),
            (set(['foo']), ['asdf']),
            ("foo",),
            ("foo", None),
            ('sdf', set(['asdf'])))
        
        starmap(assertBad, bad_vals)
        starmap(assertGood, good_vals)
