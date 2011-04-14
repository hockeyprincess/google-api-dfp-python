#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Unit tests to cover NetworkService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

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


class NetworkServiceTestV201004(unittest.TestCase):

  """Unittest suite for NetworkService using v201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  client.debug = False
  service = None
  network = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetAllNetworks(self):
    """Test whether we can fetch all networks."""
    self.assert_(isinstance(self.__class__.service.GetAllNetworks(), tuple))

  def testGetCurrentNetwork(self):
    """Test whether we can fetch current network."""
    self.__class__.network = self.__class__.service.GetCurrentNetwork()[0]
    self.assert_(isinstance(self.__class__.network, dict))

  def testUpdateNetwork(self):
    """Test whether we can update a network."""
    if not self.__class__.network:
      self.testGetCurrentNetwork()
    display_name = 'My test network'
    self.__class__.network['displayName'] = 'My test network'
    order = self.__class__.service.UpdateNetwork(self.__class__.network)
    self.assert_(isinstance(order, tuple))
    self.assertEqual(order[0]['displayName'], display_name)


class NetworkServiceTestV201010(unittest.TestCase):

  """Unittest suite for NetworkService using v201010."""

  SERVER = SERVER_V201010
  VERSION = VERSION_V201010
  client.debug = False
  service = None
  network = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetAllNetworks(self):
    """Test whether we can fetch all networks."""
    self.assert_(isinstance(self.__class__.service.GetAllNetworks(), tuple))

  def testGetCurrentNetwork(self):
    """Test whether we can fetch current network."""
    self.__class__.network = self.__class__.service.GetCurrentNetwork()[0]
    self.assert_(isinstance(self.__class__.network, dict))

  def testUpdateNetwork(self):
    """Test whether we can update a network."""
    if not self.__class__.network:
      self.testGetCurrentNetwork()
    display_name = 'My test network'
    self.__class__.network['displayName'] = 'My test network'
    order = self.__class__.service.UpdateNetwork(self.__class__.network)
    self.assert_(isinstance(order, tuple))
    self.assertEqual(order[0]['displayName'], display_name)


class NetworkServiceTestV201101(unittest.TestCase):

  """Unittest suite for NetworkService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None
  network = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetAllNetworks(self):
    """Test whether we can fetch all networks."""
    self.assert_(isinstance(self.__class__.service.GetAllNetworks(), tuple))

  def testGetCurrentNetwork(self):
    """Test whether we can fetch current network."""
    self.__class__.network = self.__class__.service.GetCurrentNetwork()[0]
    self.assert_(isinstance(self.__class__.network, dict))

  def testUpdateNetwork(self):
    """Test whether we can update a network."""
    if not self.__class__.network:
      self.testGetCurrentNetwork()
    display_name = 'My test network'
    self.__class__.network['displayName'] = 'My test network'
    order = self.__class__.service.UpdateNetwork(self.__class__.network)
    self.assert_(isinstance(order, tuple))
    self.assertEqual(order[0]['displayName'], display_name)


class NetworkServiceTestV201103(unittest.TestCase):

  """Unittest suite for NetworkService using v201103."""

  SERVER = SERVER_V201103
  VERSION = VERSION_V201103
  client.debug = False
  service = None
  network = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetAllNetworks(self):
    """Test whether we can fetch all networks."""
    self.assert_(isinstance(self.__class__.service.GetAllNetworks(), tuple))

  def testGetCurrentNetwork(self):
    """Test whether we can fetch current network."""
    self.__class__.network = self.__class__.service.GetCurrentNetwork()[0]
    self.assert_(isinstance(self.__class__.network, dict))

  def testUpdateNetwork(self):
    """Test whether we can update a network."""
    if not self.__class__.network:
      self.testGetCurrentNetwork()
    display_name = 'My test network'
    self.__class__.network['displayName'] = 'My test network'
    order = self.__class__.service.UpdateNetwork(self.__class__.network)
    self.assert_(isinstance(order, tuple))
    self.assertEqual(order[0]['displayName'], display_name)


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(NetworkServiceTestV201004))
  return suite


def makeTestSuiteV201010():
  """Set up test suite using v201010.

  Returns:
    TestSuite test suite using v201010.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(NetworkServiceTestV201010))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(NetworkServiceTestV201101))
  return suite


def makeTestSuiteV201103():
  """Set up test suite using v201103.

  Returns:
    TestSuite test suite using v201103.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(NetworkServiceTestV201103))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  suite_v201010 = makeTestSuiteV201010()
  suite_v201101 = makeTestSuiteV201101()
  suite_v201103 = makeTestSuiteV201103()
  alltests = unittest.TestSuite([suite_v201004, suite_v201010, suite_v201101,
                                 suite_v201103])
  unittest.main(defaultTest='alltests')
