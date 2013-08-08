#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import ConfigParser
import os
import stat
import sys


class MSGConfiger(object):
    """
    Supports system-specific configuration for MECO data processing.
    The site configuration file is located in ~/.meco-data-operations.cfg.
    """

    def __init__(self):
        """
        Constructor.
        """

        self._config = ConfigParser.ConfigParser()

        # Define tables that will have data inserted. Data will only be inserted
        # to tables that are defined here.
        self.insertTables = (
            'MeterData', 'RegisterData', 'RegisterRead', 'Tier', 'Register',
            'IntervalReadData', 'Interval', 'Reading', 'EventData', 'Event')

        # Check permissions on the config file. Refuse to run if the permissions
        # are not set appropriately.

        configFilePath = '~/.msg-data-operations.cfg'

        if self.isMoreThanOwnerReadableAndWritable(
                os.path.expanduser(configFilePath)):
            print "Configuration file permissions are too permissive. " \
                  "Operation will not continue."
            sys.exit()

        try:
            self._config.read(['site.cfg', os.path.expanduser(configFilePath)])
        except:
            print "Critical error: Failed to read site _config"
            sys.exit()


    def configOptionValue(self, section, option):
        """
        Get a configuration value from the local configuration file.

        :param section
        :param option
        """

        try:
            configValue = self._config.get(section, option)
            if configValue == "True":
                return True
            elif configValue == "False":
                return False
            else:
                return configValue
        except:
            print "Failed when getting _config option %s in section %s" % (
                option, section)
            sys.exit()


    def isMoreThanOwnerReadableAndWritable(self, filePath):
        """
        Determines if a file has greater permissions than owner read/write.

        :param filePath: Path to the file being tested.
        :returns: True if the permissions are greater than owner read/write,
        otherwise return False.
        """

        st = os.stat(filePath)

        # Permissions are too permissive if group or others can read,
        # write or execute.
        if bool(st.st_mode & stat.S_IRGRP) or bool(
                        st.st_mode & stat.S_IROTH) or bool(
                        st.st_mode & stat.S_IWGRP) or bool(
                        st.st_mode & stat.S_IWOTH) or bool(
                        st.st_mode & stat.S_IXGRP) or bool(
                        st.st_mode & stat.S_IXOTH):
            return True
        else:
            return False