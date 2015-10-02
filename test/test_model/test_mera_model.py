__author__ = 'Dani'

import unittest

from wmera.mera_core.labelled_model.entities import *


class TestMeraModel(unittest.TestCase):

    def test_artist_namevar(self):
        data = "http://a_source_uri.org"


        mar = MeraArtist(labelled_canonical=("katy perry", data),
                         labelled_aliases=None,
                         labelled_namevars=[("perry", data), ("katy", data)],
                         labelled_country=("USA", data))

        for namevar in mar.namevars:
            self.assertIn(namevar, ['perry', 'katy'])


        for namevar in mar.namevars_tuples:
            self.assertIn(namevar, [("perry", data), ("katy", data)])

        mar.add_namevar(("katyperr", data))

        for namevar in mar.namevars:
            self.assertIn(namevar, ['perry', 'katy', 'katyperr'])

        for namevar in mar.namevars_tuples:
            self.assertIn(namevar, [("perry", data), ("katy", data), ("katyperr", data)])

