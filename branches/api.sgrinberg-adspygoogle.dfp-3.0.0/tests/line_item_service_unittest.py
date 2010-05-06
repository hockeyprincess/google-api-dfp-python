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

"""Unit tests to cover LineItemService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import time
import unittest

from tests import HTTP_PROXY
from tests import SERVER
from tests import client


class LineItemServiceTestV201004(unittest.TestCase):

  """Unittest suite for LineItemService using v201004."""

  SERVER_V201004 = SERVER
  VERSION_V201004 = 'v201004'
  client.debug = False
  service = None
  order_id = '0'
  ad_unit_id = '0'
  line_item1 = None
  line_item2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetLineItemService(
          self.__class__.SERVER_V201004, self.__class__.VERSION_V201004,
          HTTP_PROXY)

    if self.__class__.order_id is '0':
      company = {
        'name': 'Company #%s' % time.time(),
        'type': 'ADVERTISER'
      }
      advertiser_id = client.GetCompanyService(
          self.__class__.SERVER_V201004, self.__class__.VERSION_V201004,
          HTTP_PROXY).CreateCompany(company)[0]['id']
      filter_statement = {'query': 'ORDER BY name LIMIT 500'}
      users = client.GetUserService(self.__class__.SERVER_V201004,
          self.__class__.VERSION_V201004,
          HTTP_PROXY).GetUsersByStatement(filter_statement)
      trafficker_id = '0'
      for user in users[0]['results']:
        if user['roleName'] in ('Trafficker',):
          trafficker_id = user['id']
          break
      order = {
          'advertiserId': advertiser_id,
          'currencyCode': 'USD',
          'name': 'Order #%s' % time.time(),
          'traffickerId': trafficker_id
      }
      self.__class__.order_id = client.GetOrderService(
          self.__class__.SERVER_V201004, self.__class__.VERSION_V201004,
          HTTP_PROXY).CreateOrder(order)[0]['id']

    if self.__class__.ad_unit_id is '0':
      inventory_service = client.GetInventoryService(
          self.__class__.SERVER_V201004, self.__class__.VERSION_V201004,
          HTTP_PROXY)
      filter_statement = {'query': 'WHERE parentId IS NULL LIMIT 500'}
      root_ad_unit_id = inventory_service.GetAdUnitsByStatement(
          filter_statement)[0]['results'][0]['id']
      ad_unit = {
          'name': 'Ad_Unit_%s' % str(time.time()).split('.')[0],
          'parentId': root_ad_unit_id,
          'sizes': [{'width': '300', 'height': '250'}]
      }
      self.__class__.ad_unit_id = inventory_service.CreateAdUnit(
          ad_unit)[0]['id']

  def testCreateLineItem(self):
    """Test whether we can create a line item."""
    line_item = {
        'name': 'Line item #%s' % time.time(),
        'orderId': self.__class__.order_id,
        'targeting': {
            'inventoryTargeting': {
                'targetedAdUnitIds': [self.__class__.ad_unit_id]
            }
        },
        'creativeSizes': [
            {'width': '300', 'height': '250'},
            {'width': '120', 'height': '600'}
        ],
        'lineItemType': 'STANDARD',
        'startDateTime': {
            'date': {
                'year': '2010',
                'month': '9',
                'day': '1'
            },
            'hour': '0',
            'minute': '0',
            'second': '0',
            'timeZoneID': 'America/New_York'},
        'endDateTime': {
            'date': {
                'year': '2010',
                'month': '9',
                'day': '30'
            },
            'hour': '0',
            'minute': '0',
            'second': '0',
            'timeZoneID': 'America/New_York'},
        'costType': 'CPM',
        'costPerUnit': {
            'currencyCode': 'USD',
            'microAmount': '2000000'
        },
        'creativeRotationType': 'EVEN',
        'discountType': 'PERCENTAGE',
        'unitsBought': '500000',
        'unitType': 'IMPRESSIONS'
    }
    self.assert_(isinstance(
        self.__class__.service.CreateLineItem(line_item), tuple))

  def testCreateLineItems(self):
    """Test whether we can create a list of line items."""
    line_items = [
        {
            'name': 'Line item #%s' % time.time(),
            'orderId': self.__class__.order_id,
            'targeting': {
                'inventoryTargeting': {
                    'targetedAdUnitIds': [self.__class__.ad_unit_id]
                }
            },
            'creativeSizes': [
                {'width': '300', 'height': '250'},
                {'width': '120', 'height': '600'}
            ],
            'lineItemType': 'STANDARD',
            'startDateTime': {
                'date': {
                    'year': '2010',
                    'month': '9',
                    'day': '1'
                },
                'hour': '0',
                'minute': '0',
                'second': '0',
                'timeZoneID': 'America/New_York'},
            'endDateTime': {
                'date': {
                    'year': '2010',
                    'month': '9',
                    'day': '30'
                },
                'hour': '0',
                'minute': '0',
                'second': '0',
                'timeZoneID': 'America/New_York'},
            'costType': 'CPM',
            'costPerUnit': {
                'currencyCode': 'USD',
                'microAmount': '2000000'
            },
            'creativeRotationType': 'EVEN',
            'discountType': 'PERCENTAGE',
            'unitsBought': '500000',
            'unitType': 'IMPRESSIONS'
        },
        {
            'name': 'Line item #%s' % str(time.time() + 0.01),
            'orderId': self.__class__.order_id,
            'targeting': {
                'inventoryTargeting': {
                    'targetedAdUnitIds': [self.__class__.ad_unit_id]
                }
            },
            'creativeSizes': [
                {'width': '300', 'height': '250'},
                {'width': '120', 'height': '600'}
            ],
            'lineItemType': 'STANDARD',
            'startDateTime': {
                'date': {
                    'year': '2010',
                    'month': '9',
                    'day': '1'
                },
                'hour': '0',
                'minute': '0',
                'second': '0',
                'timeZoneID': 'America/New_York'},
            'endDateTime': {
                'date': {
                    'year': '2010',
                    'month': '9',
                    'day': '30'
                },
                'hour': '0',
                'minute': '0',
                'second': '0',
                'timeZoneID': 'America/New_York'},
            'costType': 'CPM',
            'costPerUnit': {
                'currencyCode': 'USD',
                'microAmount': '2000000'
            },
            'creativeRotationType': 'EVEN',
            'discountType': 'PERCENTAGE',
            'unitsBought': '500000',
            'unitType': 'IMPRESSIONS'
        }
    ]
    line_items = self.__class__.service.CreateLineItems(line_items)
    self.__class__.line_item1 = line_items[0]
    self.__class__.line_item2 = line_items[1]
    self.assert_(isinstance(line_items, tuple))

  def testGetLineItem(self):
    """Test whether we can fetch an existing line item."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    self.assert_(isinstance(self.__class__.service.GetLineItem(
        self.__class__.line_item1['id']), tuple))

  def testGetLineItemsByStatement(self):
    """Test whether we can fetch a list of existing line items that match given
    statement."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    filter_statement = {'query': 'WHERE orderId = \'%s\' LIMIT 500'
                        % self.__class__.order_id}
    self.assert_(isinstance(
        self.__class__.service.GetLineItemsByStatement(filter_statement),
        tuple))

  def testPerformLineItemAction(self):
    """Test whether we can activate a line item."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    action = {'type': 'ActivateLineItems'}
    filter_statement = {'query': 'WHERE orderId = \'%s\' AND status = \'READY\''
                        % self.__class__.order_id}
    self.assert_(isinstance(
        self.__class__.service.PerformLineItemAction(action, filter_statement),
        tuple))

  def testUpdateLineItem(self):
    """Test whether we can update a line item."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    self.__class__.line_item1['deliveryRateType'] = 'AS_FAST_AS_POSSIBLE'
    line_item = self.__class__.service.UpdateLineItem(
        self.__class__.line_item1)
    self.assert_(isinstance(line_item, tuple))
    self.assertEqual(line_item[0]['deliveryRateType'],
                     self.__class__.line_item1['deliveryRateType'])

  def testUpdateLineItems(self):
    """Test whether we can update a list of line items."""
    if not self.__class__.line_item1 or not self.__class__.line_item2:
      self.testCreateLineItems()
    amount = '3000000'
    self.__class__.line_item1['costPerUnit']['microAmount'] = amount
    self.__class__.line_item2['costPerUnit']['microAmount'] = amount
    line_items = self.__class__.service.UpdateLineItems([
        self.__class__.line_item1, self.__class__.line_item2])
    self.assert_(isinstance(line_items, tuple))
    for line_item in line_items:
      self.assertEqual(line_item['costPerUnit']['microAmount'], amount)


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LineItemServiceTestV201004))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  alltests = unittest.TestSuite([suite_v201004])
  unittest.main(defaultTest='alltests')
