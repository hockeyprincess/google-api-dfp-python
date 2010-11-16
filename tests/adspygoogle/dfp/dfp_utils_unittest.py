#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

"""Unit tests to cover Utils."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from adspygoogle.common.Errors import ValidationError
from adspygoogle.dfp import DfpUtils
from adspygoogle.dfp.DfpSoapBuffer import DfpSoapBuffer
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201004
from tests.adspygoogle.dfp import SERVER_V201010
from tests.adspygoogle.dfp import VERSION_V201004
from tests.adspygoogle.dfp import VERSION_V201010
from tests.adspygoogle.dfp import client


class DfpUtilsTestV201004(unittest.TestCase):

  """Unittest suite for DfpUtils using v201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  client.debug = False
  TRIGGER_MSG = ('502 Server Error. The server encountered a temporary error'
                 ' and could not complete yourrequest. Please try again in 30 '
                 'seconds.')

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testError502(self):
    """Test whether we can handle and report 502 errors."""
    # Temporarily redirect STDOUT into a buffer.
    buf = DfpSoapBuffer()
    sys.stdout = buf

    html_code = Utils.ReadFile(os.path.join('data', 'http_error_502.html'))
    print html_code

    # Restore STDOUT.
    sys.stdout = sys.__stdout__

    if not buf.IsHandshakeComplete():
      data = buf.GetBufferAsStr()
    else:
      data = ''

    self.assertEqual(Utils.GetErrorFromHtml(data), self.__class__.TRIGGER_MSG)

  def testDataFileCurrencies(self):
    """Test whether csv data file with currencies is valid."""
    cols = 2
    for item in DfpUtils.GetCurrencies():
      self.assertEqual(len(item), cols)

  def testDataFileTimezones(self):
    """Test whether csv data file with timezones is valid."""
    cols = 1
    for item in DfpUtils.GetTimezones():
      self.assertEqual(len(item), cols)

  def testGetAllEntitiesByStatement(self):
    """Test whether GetAllEntitiesByStatement() does what it suppose to."""
    users = DfpUtils.GetAllEntitiesByStatement(
        client, 'User', 'ORDER BY name',
        server=self.__class__.SERVER, version=self.__class__.VERSION,
        http_proxy=HTTP_PROXY)
    self.assert_(isinstance(users, list))

  def testGetAllEntitiesByStatementWithLimit(self):
    """Test whether GetAllEntitiesByStatement() does what it suppose to do when
    LIMIT is provided as part of the query."""
    self.failUnlessRaises(ValidationError, DfpUtils.GetAllEntitiesByStatement,
        client, 'User', 'ORDER BY name LIMIT 1',
        server=self.__class__.SERVER, version=self.__class__.VERSION,
        http_proxy=HTTP_PROXY)


class DfpUtilsTestV201010(unittest.TestCase):

  """Unittest suite for DfpUtils using v201010."""

  SERVER = SERVER_V201010
  VERSION = VERSION_V201010
  client.debug = False
  TRIGGER_MSG = ('502 Server Error. The server encountered a temporary error'
                 ' and could not complete yourrequest. Please try again in 30 '
                 'seconds.')

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testError502(self):
    """Test whether we can handle and report 502 errors."""
    # Temporarily redirect STDOUT into a buffer.
    buf = DfpSoapBuffer()
    sys.stdout = buf

    html_code = Utils.ReadFile(os.path.join('data', 'http_error_502.html'))
    print html_code

    # Restore STDOUT.
    sys.stdout = sys.__stdout__

    if not buf.IsHandshakeComplete():
      data = buf.GetBufferAsStr()
    else:
      data = ''

    self.assertEqual(Utils.GetErrorFromHtml(data), self.__class__.TRIGGER_MSG)

  def testDataFileCurrencies(self):
    """Test whether csv data file with currencies is valid."""
    cols = 2
    for item in DfpUtils.GetCurrencies():
      self.assertEqual(len(item), cols)

  def testDataFileTimezones(self):
    """Test whether csv data file with timezones is valid."""
    cols = 1
    for item in DfpUtils.GetTimezones():
      self.assertEqual(len(item), cols)

  def testGetAllEntitiesByStatement(self):
    """Test whether GetAllEntitiesByStatement() does what it suppose to."""
    users = DfpUtils.GetAllEntitiesByStatement(
        client, 'User', 'ORDER BY name',
        server=self.__class__.SERVER, version=self.__class__.VERSION,
        http_proxy=HTTP_PROXY)
    self.assert_(isinstance(users, list))

  def testGetAllEntitiesByStatementWithLimit(self):
    """Test whether GetAllEntitiesByStatement() does what it suppose to do when
    LIMIT is provided as part of the query."""
    self.failUnlessRaises(ValidationError, DfpUtils.GetAllEntitiesByStatement,
        client, 'User', 'ORDER BY name LIMIT 1',
        server=self.__class__.SERVER, version=self.__class__.VERSION,
        http_proxy=HTTP_PROXY)


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpUtilsTestV201004))
  return suite


def makeTestSuiteV201010():
  """Set up test suite using v201010.

  Returns:
    TestSuite test suite using v201010.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpUtilsTestV201010))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  suite_v201010 = makeTestSuiteV201010()
  alltests = unittest.TestSuite([suite_v201004, suite_v201010])
  unittest.main(defaultTest='alltests')
