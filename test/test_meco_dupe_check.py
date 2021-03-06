#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from meco_dupe_check import MECODupeChecker
from meco_xml_parser import MECOXMLParser
from msg_db_connector import MSGDBConnector
from msg_db_util import MSGDBUtil


class TestMECODupeChecker(unittest.TestCase):
    """
    Unit tests for duplicate checking.
    """

    def setUp(self):
        self.dupeChecker = MECODupeChecker()
        self.p = MECOXMLParser(True) # run in testing mode
        self.dbConnect = MSGDBConnector(True)
        self.dbUtil = MSGDBUtil()
        self.conn = self.dbConnect.connectDB()
        self.cur = self.conn.cursor()

    def testInit(self):
        self.assertEqual(self.dupeChecker.__class__.__name__, "MECODupeChecker",
                         "Dupe checker has been created.")

    def testFindIndividualDupe(self):
        """
        Find a duplicate record when only one exists.
        """
        self.dbUtil.eraseTestMeco()

        self.p.filename = "../../test-data/meco_v3-energy-test-data.xml"
        fileObject = open(self.p.filename, "rb")
        self.p.parseXML(fileObject, True)

        self.assertTrue(
            self.dupeChecker.readingBranchDupeExists(self.conn, '100000',
                                                     '2013-04-08 00:30:00',
                                                     '1', True),
            "Record should already exist")

    def testLoadOnTop(self):
        """
        If the same data set is loaded in succession,
        all values will be duplicated. Verify that this is true.

        This is no longer possible as
        duplicates are dropped before insertion.
        """

        pass

    def testLoadSingleMissingEntry(self):
        """
        A reading will be inserted into the database where the reading does
        not currently exist as determined by the
        MeterName-IntervalEndTime-Channel tuple.
        """

        pass

    def tearDown(self):
        self.dbConnect.closeDB(self.conn)

if __name__ == '__main__':
    unittest.main()

