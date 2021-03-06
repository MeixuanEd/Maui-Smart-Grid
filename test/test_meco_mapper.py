#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2013, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github' \
              '.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/BSD' \
              '-LICENSE.txt'

import unittest
from meco_mapper import MECOMapper
from msg_configer import MSGConfiger


class TestMECOMapper(unittest.TestCase):
    """
    Unit tests for MECO Mapper.
    """

    def setUp(self):
        self.m = MECOMapper()
        self.testColumns = self.m.dbColsMeterData.values()
        self.testLabels = self.m.dbColsMeterData.keys()
        self.testTableName = 'MeterData'
        self.config = MSGConfiger()

    def testMECOMapperCanBeInited(self):
        localMapper = MECOMapper()
        self.assertIsInstance(self.m, type(localMapper))

    def testMappingReturnsAListWithMembersMoreThanZero(self):
        self.assertTrue(len(self.testColumns) > 0)

    def test_fkey_mappings(self):
        """
        Verify fkey mappings for tables.
        """

        print "test_fkey_mappings:"
        errors = 0
        # @todo Add other fkeys here.
        fkeys = {'RegisterData': 'meter_data_id'}

        for table in self.config.insertTables:
            try:
                print self.m.dbColumnsForTable(table)['_fkey']
                if self.m.dbColumnsForTable(table)['_fkey'] != fkeys[table]:
                    errors += 1
            except:
                # The table doesn't have an fkey.
                pass
        self.assertLess(errors, 1)

    # @todo finish writing this test
    def testMappingIsValidForMeterData(self):
        """
        Compare columns that are mapped for given data labels.
        """

        # Given labels from the source data, map them to DB column names.
        srcDataLabels = ('MacID', 'MeterName', 'UtilDeviceID')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
