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

import sys
sys.path.append('..')
import time
import unittest

from tests import HTTP_PROXY
from tests import SERVER
from tests import client


class InventoryServiceTestV201002(unittest.TestCase):

  """Unittest suite for InventoryService using v201002."""

  SERVER_V201002 = SERVER
  VERSION_V201002 = 'v201002'
  client.debug = False
  service = None
  root_ad_unit_id = '0'
  ad_unit = None
  ad_unit = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetInventoryService(
          self.__class__.SERVER_V201002, self.__class__.VERSION_V201002,
          HTTP_PROXY)

    if self.__class__.root_ad_unit_id is '0':
      filter = {'text': 'WHERE parentId IS NULL LIMIT 500'}
      self.__class__.root_ad_unit_id = \
          self.__class__.service.GetAdUnitsByFilter(
              filter)[0]['results'][0]['id']

  def testCreateAdUnit(self):
    """Test whether we can create an ad unit."""
    ad_unit = {
        'name': 'Ad_Unit_%s' % str(time.time()).split('.')[0],
        'parentId': self.__class__.root_ad_unit_id,
        'sizes': [{'width': '300', 'height': '250'}]
    }
    self.assert_(isinstance(
        self.__class__.service.CreateAdUnit(ad_unit), tuple))

  def testCreateAdUnits(self):
    """Test whether we can create a list of ad units."""
    ad_units = [
        {
            'name': 'Ad_Unit_%s' % str(time.time()).split('.')[0],
            'parentId': self.__class__.root_ad_unit_id,
            'sizes': [{'width': '300', 'height': '250'}]
        },
        {
            'name': 'Ad_Unit_%s' % str(time.time() + 1).split('.')[0],
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

  def testGetAdUnitsByFilter(self):
    """Test whether we can fetch a list of existing ad units that match given
    filter."""
    filter = {'text': 'WHERE parentId IS NULL LIMIT 500'}
    self.assert_(isinstance(
        self.__class__.service.GetAdUnitsByFilter(filter), tuple))

  def testPerformAdUnitAction(self):
    """Test whether we can deactivate an ad unit."""
    action = {'type': 'DeactivateAdUnits'}
    filter = {'text': 'WHERE status = \'ACTIVE\''}
    self.assert_(isinstance(
        self.__class__.service.PerformAdUnitAction(action, filter), tuple))

  def testUpdateAdUnit(self):
    """Test whether we can update an ad unit."""
    if self.__class__.ad_unit1 is None:
      self.testCreateAdUnits()
    size = {'width': '728', 'height': '90'}
    self.__class__.ad_unit1['sizes'] = [size]
    ad_unit = self.__class__.service.UpdateAdUnit(self.__class__.ad_unit1)
    self.assert_(isinstance(ad_unit, tuple))
    self.assertEqual(ad_unit[0]['sizes'][0], size)

  def testUpdateAdUnits(self):
    """Test whether we can update a list of ad units."""
    if self.__class__.ad_unit1 is None or self.__class__.ad_unit2 is None:
      self.testCreateAdUnits()
    size = {'width': '728', 'height': '90'}
    self.__class__.ad_unit1['sizes'] = [size]
    self.__class__.ad_unit2['sizes'] = [size]
    ad_units = self.__class__.service.UpdateAdUnits(
        [self.__class__.ad_unit1, self.__class__.ad_unit2])
    self.assert_(isinstance(ad_units, tuple))
    for ad_unit in ad_units:
      self.assertEqual(ad_unit['sizes'][0], size)


def makeTestSuiteV201002():
  """Set up test suite using v201002.

  Returns:
    TestSuite test suite using v201002.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(InventoryServiceTestV201002))
  return suite


if __name__ == '__main__':
  suite_v201002 = makeTestSuiteV201002()
  alltests = unittest.TestSuite([suite_v201002])
  unittest.main(defaultTest='alltests')
