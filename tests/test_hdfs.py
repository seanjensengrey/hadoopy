#!/usr/bin/env python
# (C) Copyright 2010 Andrew Miller
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Andrew Miller <amiller@dappervision.com'
__license__ = 'GPL V3'

import subprocess
import time
import unittest

import hadoopy


class TestHDFS(unittest.TestCase):

    def __init__(self, *args, **kw):
        super(TestHDFS, self).__init__(*args, **kw)
        self.data_path = 'hadoopy-test-data/%f/' % (time.time())
        self.fn = 'wc-input-alice.txt'
        self.file_path = self.data_path + self.fn
        self.nonsense_path = self.data_path + '93f8h93'

        # Upload a test file
        cmd = 'hadoop fs -put %s %s' % (self.fn, self.file_path)
        subprocess.check_call(cmd.split())

    def test_ls(self):
        ls_output = hadoopy.ls(self.data_path)
        self.assertTrue(ls_output[0].endswith(self.file_path))

    def test_cat(self):
        cat_output = [_ for _ in hadoopy.cat(self.file_path)]
        line = (331, 'Title: Alice\'s Adventures in Wonderland')
        self.assertTrue(line in cat_output)

    def test_err(self):
        self.assertRaises(IOError, hadoopy.ls, self.nonsense_path)
        self.assertRaises(IOError, hadoopy.cat(self.nonsense_path).next)


if __name__ == '__main__':
    unittest.main()
