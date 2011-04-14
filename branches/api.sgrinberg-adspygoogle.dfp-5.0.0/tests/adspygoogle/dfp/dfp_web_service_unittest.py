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

"""Unit tests to cover DfpWebService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import thread
import threading
import unittest

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import Utils
from adspygoogle.dfp.DfpErrors import DfpApiError
from adspygoogle.dfp.DfpWebService import DfpWebService
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201004
from tests.adspygoogle.dfp import SERVER_V201010
from tests.adspygoogle.dfp import VERSION_V201004
from tests.adspygoogle.dfp import VERSION_V201010
from tests.adspygoogle.dfp import client


class DfpWebServiceTestV201004(unittest.TestCase):

  """Unittest suite for DfpWebService using v201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    self.assert_(isinstance(client.GetUserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetUsersByStatement(
            filter_statement), tuple))

  def testCallMethodDirect(self):
    """Test whether we can call an API method directly."""
    headers = client.GetAuthCredentials()
    config = client.GetConfigValues()
    url = '/'.join([DfpWebServiceTestV201004.SERVER,
                   'apis/ads/publisher/v201004', 'UserService'])
    op_config = {
        'server': self.__class__.SERVER,
        'version': self.__class__.VERSION,
        'http_proxy': HTTP_PROXY
    }

    lock = thread.allocate_lock()
    service = DfpWebService(headers, config, op_config, url, lock)
    method_name = 'getAllRoles'
    if config['soap_lib'] == SOAPPY:
      self.assert_(isinstance(service.CallMethod(method_name, (),
                                                 'UserService'), tuple))
    elif config['soap_lib'] == ZSI:
      web_services = __import__(
          'adspygoogle.dfp.zsi.v201004.UserService_services',
          globals(), locals(), [''])
      loc = web_services.UserServiceLocator()
      request = eval('web_services.%sRequest()' % method_name)
      self.assert_(isinstance(service.CallMethod(
          method_name,
          (({'filterStatement': {'query': 'ORDER BY name LIMIT 500'}},)),
          'User', loc, request), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getusersbystatement.xml'))
    url = '/apis/ads/publisher/v201004/UserService'
    http_proxy = None

    self.failUnlessRaises(DfpApiError, client.CallRawMethod, soap_message, url,
                          self.__class__.SERVER, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201004()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV201004(threading.Thread):

  """Creates TestThread using v201004.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    statement = {'query': 'ORDER BY name LIMIT 500'}
    DfpWebServiceTestV201004.res.append(client.GetUserService(
        DfpWebServiceTestV201004.SERVER, DfpWebServiceTestV201004.VERSION,
        HTTP_PROXY).GetUsersByStatement(statement))


class DfpWebServiceTestV201010(unittest.TestCase):

  """Unittest suite for DfpWebService using v201010."""

  SERVER = SERVER_V201010
  VERSION = VERSION_V201010
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    self.assert_(isinstance(client.GetUserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetUsersByStatement(
            filter_statement), tuple))

  def testCallMethodDirect(self):
    """Test whether we can call an API method directly."""
    headers = client.GetAuthCredentials()
    config = client.GetConfigValues()
    url = '/'.join([DfpWebServiceTestV201010.SERVER,
                   'apis/ads/publisher/v201010', 'UserService'])
    op_config = {
        'server': self.__class__.SERVER,
        'version': self.__class__.VERSION,
        'http_proxy': HTTP_PROXY
    }

    lock = thread.allocate_lock()
    service = DfpWebService(headers, config, op_config, url, lock)
    method_name = 'getAllRoles'
    if config['soap_lib'] == SOAPPY:
      self.assert_(isinstance(service.CallMethod(method_name, (),
                                                 'UserService'), tuple))
    elif config['soap_lib'] == ZSI:
      web_services = __import__(
          'adspygoogle.dfp.zsi.v201010.UserService_services',
          globals(), locals(), [''])
      loc = web_services.UserServiceLocator()
      request = eval('web_services.%sRequest()' % method_name)
      self.assert_(isinstance(service.CallMethod(
          method_name,
          (({'filterStatement': {'query': 'ORDER BY name LIMIT 500'}},)),
          'User', loc, request), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getusersbystatement.xml'))
    url = '/apis/ads/publisher/v201004/UserService'
    http_proxy = None

    self.failUnlessRaises(DfpApiError, client.CallRawMethod, soap_message, url,
                          self.__class__.SERVER, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201010()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV201010(threading.Thread):

  """Creates TestThread using v201010.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    statement = {'query': 'ORDER BY name LIMIT 500'}
    DfpWebServiceTestV201010.res.append(client.GetUserService(
        DfpWebServiceTestV201010.SERVER, DfpWebServiceTestV201010.VERSION,
        HTTP_PROXY).GetUsersByStatement(statement))


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpWebServiceTestV201004))
  return suite


def makeTestSuiteV201010():
  """Set up test suite using v201010.

  Returns:
    TestSuite test suite using v201010.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpWebServiceTestV201010))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  suite_v201010 = makeTestSuiteV201010()
  alltests = unittest.TestSuite([suite_v201004, suite_v201010])
  unittest.main(defaultTest='alltests')
