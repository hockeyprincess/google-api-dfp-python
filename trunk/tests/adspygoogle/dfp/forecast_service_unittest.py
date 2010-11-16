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

"""Unit tests to cover ForecastService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201004
from tests.adspygoogle.dfp import SERVER_V201010
from tests.adspygoogle.dfp import VERSION_V201004
from tests.adspygoogle.dfp import VERSION_V201010
from tests.adspygoogle.dfp import client


class ForecastServiceTestV201004(unittest.TestCase):

  """Unittest suite for ForecastService using v201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  client.debug = False
  service = None
  order_id = '0'
  ad_unit_id = '0'
  line_item_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetForecastService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.order_id == '0':
      company = {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      }
      advertiser_id = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCompany(company)[0]['id']
      filter_statement = {'query': 'ORDER BY name LIMIT 500'}
      users = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetUsersByStatement(filter_statement)
      trafficker_id = '0'
      for user in users[0]['results']:
        if user['roleName'] in ('Trafficker',):
          trafficker_id = user['id']
          break
      order = {
          'advertiserId': advertiser_id,
          'currencyCode': 'USD',
          'name': 'Order #%s' % Utils.GetUniqueName(),
          'traffickerId': trafficker_id
      }
      self.__class__.order_id = client.GetOrderService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateOrder(order)[0]['id']

    if self.__class__.ad_unit_id == '0':
      inventory_service = client.GetInventoryService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      network_service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      root_ad_unit_id = \
          network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']
      ad_unit = {
          'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
          'parentId': root_ad_unit_id,
          'sizes': [{'width': '300', 'height': '250'}],
          'description': 'Ad unit description.',
          'targetWindow': 'BLANK'
      }
      self.__class__.ad_unit_id = inventory_service.CreateAdUnit(
          ad_unit)[0]['id']

    if self.__class__.line_item_id == '0':
      line_item_service = client.GetLineItemService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      line_item = {
          'name': 'Line item #%s' % Utils.GetUniqueName(),
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
                  'year': '2011',
                  'month': '9',
                  'day': '1'
              },
              'hour': '0',
              'minute': '0',
              'second': '0'
          },
          'endDateTime': {
              'date': {
                  'year': '2011',
                  'month': '9',
                  'day': '30'
              },
              'hour': '0',
              'minute': '0',
              'second': '0'
          },
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
      self.__class__.line_item_id = line_item_service.CreateLineItem(
          line_item)[0]['id']

  def testGetForecast(self):
    """Test whether we can get a forecast for given line item."""
    line_item = {
        'name': 'Line item #%s' % Utils.GetUniqueName(),
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
                'year': '2011',
                'month': '9',
                'day': '1'
            },
            'hour': '0',
            'minute': '0',
            'second': '0'
        },
        'endDateTime': {
            'date': {
                'year': '2011',
                'month': '9',
                'day': '30'
            },
            'hour': '0',
            'minute': '0',
            'second': '0'
        },
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
    self.assert_(isinstance(self.__class__.service.GetForecast(
        line_item), tuple))

  def testGetForecastById(self):
    """Test whether we can get a forecast for existing line item."""
    self.assert_(isinstance(self.__class__.service.GetForecastById(
        self.__class__.line_item_id), tuple))


class ForecastServiceTestV201010(unittest.TestCase):

  """Unittest suite for ForecastService using v201010."""

  SERVER = SERVER_V201010
  VERSION = VERSION_V201010
  client.debug = False
  service = None
  order_id = '0'
  ad_unit_id = '0'
  line_item_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetForecastService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.order_id == '0':
      company = {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      }
      advertiser_id = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCompany(company)[0]['id']
      filter_statement = {'query': 'ORDER BY name LIMIT 500'}
      users = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetUsersByStatement(filter_statement)
      trafficker_id = '0'
      for user in users[0]['results']:
        if user['roleName'] in ('Trafficker',):
          trafficker_id = user['id']
          break
      order = {
          'advertiserId': advertiser_id,
          'currencyCode': 'USD',
          'name': 'Order #%s' % Utils.GetUniqueName(),
          'traffickerId': trafficker_id
      }
      self.__class__.order_id = client.GetOrderService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateOrder(order)[0]['id']

    if self.__class__.ad_unit_id == '0':
      inventory_service = client.GetInventoryService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      filter_statement = {'query': 'WHERE parentId IS NULL LIMIT 500'}
      root_ad_unit_id = inventory_service.GetAdUnitsByStatement(
          filter_statement)[0]['results'][0]['id']
      ad_unit = {
          'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
          'parentId': root_ad_unit_id,
          'sizes': [{'width': '300', 'height': '250'}],
          'description': 'Ad unit description.',
          'targetWindow': 'BLANK'
      }
      self.__class__.ad_unit_id = inventory_service.CreateAdUnit(
          ad_unit)[0]['id']

    if self.__class__.line_item_id == '0':
      line_item_service = client.GetLineItemService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      line_item = {
          'name': 'Line item #%s' % Utils.GetUniqueName(),
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
                  'year': '2011',
                  'month': '9',
                  'day': '1'
              },
              'hour': '0',
              'minute': '0',
              'second': '0'
          },
          'endDateTime': {
              'date': {
                  'year': '2011',
                  'month': '9',
                  'day': '30'
              },
              'hour': '0',
              'minute': '0',
              'second': '0'
          },
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
      self.__class__.line_item_id = line_item_service.CreateLineItem(
          line_item)[0]['id']

  def testGetForecast(self):
    """Test whether we can get a forecast for given line item."""
    line_item = {
        'name': 'Line item #%s' % Utils.GetUniqueName(),
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
                'year': '2011',
                'month': '9',
                'day': '1'
            },
            'hour': '0',
            'minute': '0',
            'second': '0'
        },
        'endDateTime': {
            'date': {
                'year': '2011',
                'month': '9',
                'day': '30'
            },
            'hour': '0',
            'minute': '0',
            'second': '0'
        },
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
    self.assert_(isinstance(self.__class__.service.GetForecast(
        line_item), tuple))

  def testGetForecastById(self):
    """Test whether we can get a forecast for existing line item."""
    self.assert_(isinstance(self.__class__.service.GetForecastById(
        self.__class__.line_item_id), tuple))


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ForecastServiceTestV201004))
  return suite


def makeTestSuiteV201010():
  """Set up test suite using v201010.

  Returns:
    TestSuite test suite using v201010.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ForecastServiceTestV201010))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  suite_v201010 = makeTestSuiteV201010()
  alltests = unittest.TestSuite([suite_v201004, suite_v201010])
  unittest.main(defaultTest='alltests')
