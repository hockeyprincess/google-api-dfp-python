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
sys.path.append('..')
import unittest

from dfp_api import Utils
from dfp_api.SoapBuffer import SoapBuffer
from tests import HTTP_PROXY
from tests import SERVER
from tests import client


class UtilsTestV201004(unittest.TestCase):

  """Unittest suite for Utils using v201004."""

  SERVER_V201004 = SERVER
  VERSION_V201004 = 'v201004'
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
    buf = SoapBuffer()
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
    for item in Utils.GetCurrencies():
      self.assertEqual(len(item), cols)

  def testDataFileTimezones(self):
    """Test whether csv data file with timezones is valid."""
    cols = 1
    for item in Utils.GetTimezones():
      self.assertEqual(len(item), cols)

  def testGetAllEntitiesByStatement(self):
    """Test whether GetAllEntitiesByStatement() does what it suppose to."""
    users = Utils.GetAllEntitiesByStatement(
        client, 'User', 'ORDER BY name',
        server=self.__class__.SERVER_V201004,
        version=self.__class__.VERSION_V201004,
        http_proxy=HTTP_PROXY)
    self.assert_(isinstance(users, list))


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UtilsTestV201004))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  alltests = unittest.TestSuite([suite_v201004])
  unittest.main(defaultTest='alltests')
