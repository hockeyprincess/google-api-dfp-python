#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Unit tests to cover InventoryService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201004
from tests.adspygoogle.dfp import VERSION_V201004
from tests.adspygoogle.dfp import client


class InventoryServiceTestV201004(unittest.TestCase):

  """Unittest suite for InventoryService using v201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  client.debug = False
  service = None
  root_ad_unit_id = '0'
  ad_unit1 = None
  ad_unit2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetInventoryService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.root_ad_unit_id == '0':
      filter_statement = {'query': 'WHERE parentId IS NULL LIMIT 500'}
      self.__class__.root_ad_unit_id = \
          self.__class__.service.GetAdUnitsByStatement(
              filter_statement)[0]['results'][0]['id']

  def testCreateAdUnit(self):
    """Test whether we can create an ad unit."""
    ad_unit = {
        'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
        'parentId': self.__class__.root_ad_unit_id,
        'sizes': [{'width': '300', 'height': '250'}]
    }
    self.assert_(isinstance(
        self.__class__.service.CreateAdUnit(ad_unit), tuple))

  def testCreateAdUnits(self):
    """Test whether we can create a list of ad units."""
    ad_units = [
        {
            'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
            'parentId': self.__class__.root_ad_unit_id,
            'sizes': [{'width': '300', 'height': '250'}]
        },
        {
            'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
            'parentId': self.__class__.root_ad_unit_id,
            'sizes': [{'width': '300', 'height': '250'}]
        }
    ]
    ad_units = self.__class__.service.CreateAdUnits(ad_units)
    self.__class__.ad_unit1 = ad_units[0]
    self.__class__.ad_unit2 = ad_units[1]
    self.assert_(isinstance(ad_units, tuple))

  def testGetAdUnit(self):
    """Test whether we can fetch an existing ad unit."""
    if self.__class__.ad_unit1 is None:
      self.testCreateAdUnits()
    self.assert_(isinstance(self.__class__.service.GetAdUnit(
        self.__class__.ad_unit1['id']), tuple))

  def testGetAdUnitsByStatement(self):
    """Test whether we can fetch a list of existing ad units that match given
    statement."""
    filter_statement = {'query': 'WHERE parentId IS NULL LIMIT 500'}
    self.assert_(isinstance(
        self.__class__.service.GetAdUnitsByStatement(filter_statement), tuple))

  def testPerformAdUnitAction(self):
    """Test whether we can deactivate an ad unit."""
    action = {'type': 'DeactivateAdUnits'}
    filter_statement = {'query': 'WHERE status = \'ACTIVE\''}
    self.assert_(isinstance(
        self.__class__.service.PerformAdUnitAction(action, filter_statement),
        tuple))

  def testUpdateAdUnit(self):
    """Test whether we can update an ad unit."""
    if self.__class__.ad_unit1 is None:
      self.testCreateAdUnits()
    size = {'width': '728', 'isAspectRatio': 'false', 'height': '90'}
    self.__class__.ad_unit1['sizes'] = [size]
    ad_unit = self.__class__.service.UpdateAdUnit(self.__class__.ad_unit1)
    self.assert_(isinstance(ad_unit, tuple))
    self.assertEqual(ad_unit[0]['sizes'][0], size)

  def testUpdateAdUnits(self):
    """Test whether we can update a list of ad units."""
    if self.__class__.ad_unit1 is None or self.__class__.ad_unit2 is None:
      self.testCreateAdUnits()
    size = {'width': '728', 'isAspectRatio': 'false', 'height': '90'}
    self.__class__.ad_unit1['sizes'] = [size]
    self.__class__.ad_unit2['sizes'] = [size]
    ad_units = self.__class__.service.UpdateAdUnits(
        [self.__class__.ad_unit1, self.__class__.ad_unit2])
    self.assert_(isinstance(ad_units, tuple))
    for ad_unit in ad_units:
      self.assertEqual(ad_unit['sizes'][0], size)


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(InventoryServiceTestV201004))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  alltests = unittest.TestSuite([suite_v201004])
  unittest.main(defaultTest='alltests')
