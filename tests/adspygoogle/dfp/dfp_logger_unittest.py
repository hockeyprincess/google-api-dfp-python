#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests to cover Logger."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import logging
import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201004
from tests.adspygoogle.dfp import SERVER_V201010
from tests.adspygoogle.dfp import SERVER_V201101
from tests.adspygoogle.dfp import SERVER_V201103
from tests.adspygoogle.dfp import VERSION_V201004
from tests.adspygoogle.dfp import VERSION_V201010
from tests.adspygoogle.dfp import VERSION_V201101
from tests.adspygoogle.dfp import VERSION_V201103
from tests.adspygoogle.dfp import client


class DfpLoggerTestV201004(unittest.TestCase):

  """Unittest suite for Logger using v201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  TMP_LOG = os.path.join('..', '..', '..', 'logs', 'logger_unittest.log')
  DEBUG_MSG1 = 'Message before call to an API method.'
  DEBUG_MSG2 = 'Message after call to an API method.'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testUpperStackLogging(self):
    """Tests whether we can define logger at client level and log before and
    after the API request is made.
    """
    logger = logging.getLogger(self.__class__.__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(self.__class__.TMP_LOG)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Clean up temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)

    logger.debug(self.__class__.DEBUG_MSG1)
    user_service = client.GetUserService(
        self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
    user_service.GetAllRoles()
    logger.debug(self.__class__.DEBUG_MSG2)

    data = Utils.ReadFile(self.__class__.TMP_LOG)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG1), 0)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG2),
                     len(self.__class__.DEBUG_MSG1) + 1)

    # Clean up and remove temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)
    os.remove(self.__class__.TMP_LOG)


class DfpLoggerTestV201010(unittest.TestCase):

  """Unittest suite for Logger using v201010."""

  SERVER = SERVER_V201010
  VERSION = VERSION_V201010
  TMP_LOG = os.path.join('..', '..', '..', 'logs', 'logger_unittest.log')
  DEBUG_MSG1 = 'Message before call to an API method.'
  DEBUG_MSG2 = 'Message after call to an API method.'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testUpperStackLogging(self):
    """Tests whether we can define logger at client level and log before and
    after the API request is made.
    """
    logger = logging.getLogger(self.__class__.__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(self.__class__.TMP_LOG)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Clean up temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)

    logger.debug(self.__class__.DEBUG_MSG1)
    user_service = client.GetUserService(
        self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
    user_service.GetAllRoles()
    logger.debug(self.__class__.DEBUG_MSG2)

    data = Utils.ReadFile(self.__class__.TMP_LOG)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG1), 0)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG2),
                     len(self.__class__.DEBUG_MSG1) + 1)

    # Clean up and remove temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)
    os.remove(self.__class__.TMP_LOG)


class DfpLoggerTestV201101(unittest.TestCase):

  """Unittest suite for Logger using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  TMP_LOG = os.path.join('..', '..', '..', 'logs', 'logger_unittest.log')
  DEBUG_MSG1 = 'Message before call to an API method.'
  DEBUG_MSG2 = 'Message after call to an API method.'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testUpperStackLogging(self):
    """Tests whether we can define logger at client level and log before and
    after the API request is made.
    """
    logger = logging.getLogger(self.__class__.__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(self.__class__.TMP_LOG)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Clean up temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)

    logger.debug(self.__class__.DEBUG_MSG1)
    user_service = client.GetUserService(
        self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
    user_service.GetAllRoles()
    logger.debug(self.__class__.DEBUG_MSG2)

    data = Utils.ReadFile(self.__class__.TMP_LOG)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG1), 0)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG2),
                     len(self.__class__.DEBUG_MSG1) + 1)

    # Clean up and remove temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)
    os.remove(self.__class__.TMP_LOG)


class DfpLoggerTestV201103(unittest.TestCase):

  """Unittest suite for Logger using v201103."""

  SERVER = SERVER_V201103
  VERSION = VERSION_V201103
  TMP_LOG = os.path.join('..', '..', '..', 'logs', 'logger_unittest.log')
  DEBUG_MSG1 = 'Message before call to an API method.'
  DEBUG_MSG2 = 'Message after call to an API method.'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testUpperStackLogging(self):
    """Tests whether we can define logger at client level and log before and
    after the API request is made.
    """
    logger = logging.getLogger(self.__class__.__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(self.__class__.TMP_LOG)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Clean up temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)

    logger.debug(self.__class__.DEBUG_MSG1)
    user_service = client.GetUserService(
        self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
    user_service.GetAllRoles()
    logger.debug(self.__class__.DEBUG_MSG2)

    data = Utils.ReadFile(self.__class__.TMP_LOG)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG1), 0)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG2),
                     len(self.__class__.DEBUG_MSG1) + 1)

    # Clean up and remove temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)
    os.remove(self.__class__.TMP_LOG)


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpLoggerTestV201004))
  return suite


def makeTestSuiteV201010():
  """Set up test suite using v201010.

  Returns:
    TestSuite test suite using v201010.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpLoggerTestV201010))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpLoggerTestV201101))
  return suite


def makeTestSuiteV201103():
  """Set up test suite using v201103.

  Returns:
    TestSuite test suite using v201103.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpLoggerTestV201103))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  suite_v201010 = makeTestSuiteV201010()
  suite_v201101 = makeTestSuiteV201101()
  suite_v201103 = makeTestSuiteV201103()
  alltests = unittest.TestSuite([suite_v201004, suite_v201010, suite_v201101,
                                 suite_v201103])
  unittest.main(defaultTest='alltests')
