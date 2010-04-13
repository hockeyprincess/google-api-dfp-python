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

"""Unit tests to cover WebService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append('..')
import thread
import threading
import unittest

from dfp_api import Utils
from dfp_api.Errors import ApiError
from dfp_api.WebService import WebService
from tests import HTTP_PROXY
from tests import SERVER
from tests import client


class WebServiceTestV201002(unittest.TestCase):

  """Unittest suite for WebService using v201002."""

  SERVER_V201002 = SERVER
  VERSION_V201002 = 'v201002'
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    filter = {'text': 'ORDER BY name LIMIT 500'}
    self.assert_(isinstance(client.GetUserService(self.__class__.SERVER_V201002,
        self.__class__.VERSION_V201002, HTTP_PROXY).GetUsersByFilter(filter),
        tuple))

  def testCallMethodDirectV201002(self):
    """Test whether we can call an API method directly."""
    headers = client.GetAuthCredentials()
    config = client.GetConfigValues()
    url = os.path.join(WebServiceTestV201002.SERVER_V201002,
                       'apis/ads/publisher/v201002', 'UserService')
    op_config = {
        'server': self.__class__.SERVER_V201002,
        'version': self.__class__.VERSION_V201002,
        'http_proxy': HTTP_PROXY
    }

    lock = thread.allocate_lock()
    service = WebService(headers, config, op_config, url, lock)
    method_name = 'getUsersByFilter'
    web_services = __import__(
        'dfp_api.zsi_toolkit.v201002.UserService_services',
        globals(), locals(), [''])
    loc = web_services.UserServiceLocator()
    request = eval('web_services.%sRequest()' % method_name)
    self.assert_(isinstance(service.CallMethod(
        method_name, (({'filter': {'text': 'ORDER BY name LIMIT 500'}},)),
        'User', loc, request), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join(os.getcwd(), 'data', 'request_getusersbyfilter.xml'))
    url = '/apis/ads/publisher/v201002/UserService'
    http_proxy = None

    self.failUnlessRaises(ApiError, client.CallRawMethod, soap_message, url,
                          http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201002()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV201002(threading.Thread):

  """Creates TestThread using v201002.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    filter = {'text': 'ORDER BY name LIMIT 500'}
    WebServiceTestV201002.res.append(client.GetUserService(
        WebServiceTestV201002.SERVER_V201002,
        WebServiceTestV201002.VERSION_V201002,
        HTTP_PROXY).GetUsersByFilter(filter))


def makeTestSuiteV201002():
  """Set up test suite using v201002.

  Returns:
    TestSuite test suite using v201002.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(WebServiceTestV201002))
  return suite


if __name__ == '__main__':
  suite_v201002 = makeTestSuiteV201002()
  alltests = unittest.TestSuite([suite_v201002])
  unittest.main(defaultTest='alltests')
