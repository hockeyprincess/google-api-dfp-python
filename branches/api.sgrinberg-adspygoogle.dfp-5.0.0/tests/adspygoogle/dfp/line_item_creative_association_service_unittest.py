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

"""Unit tests to cover LineItemCreativeAssociationService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import base64
import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201004
from tests.adspygoogle.dfp import SERVER_V201010
from tests.adspygoogle.dfp import VERSION_V201004
from tests.adspygoogle.dfp import VERSION_V201010
from tests.adspygoogle.dfp import client


class LicaServiceTestV201004(unittest.TestCase):

  """Unittest suite for LineItemCreativeAssociationService using V201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  client.debug = False
  service = None
  creative1 = None
  creative2 = None
  creative3 = None
  line_item_id = None
  IMAGE_DATA = open(os.path.join('data', 'medium_rectangle.jpg').replace(
      '\\', '/'), 'r').read()
  if client.soap_lib == SOAPPY:
    IMAGE_DATA = base64.encodestring(IMAGE_DATA)
  lica1 = None
  lica2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetLineItemCreativeAssociationService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (not self.__class__.creative1 or not self.__class__.creative2 or
        not self.__class__.creative3):
      company = {
        'name': 'Company #%s' % Utils.GetUniqueName(),
        'type': 'ADVERTISER'
      }
      advertiser_id = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCompany(company)[0]['id']
      creatives = []
      for i in xrange(3):
        creatives.append({
            'type': 'ImageCreative',
            'name': 'Image Creative #%s' % Utils.GetUniqueName(),
            'advertiserId': advertiser_id,
            'destinationUrl': 'http://google.com',
            'imageName': 'image.jpg',
            'imageByteArray': self.__class__.IMAGE_DATA,
            'size': {'width': '300', 'height': '250'}
        })
      creatives = client.GetCreativeService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCreatives(creatives)
      self.__class__.creative1 = creatives[0]
      self.__class__.creative2 = creatives[1]
      self.__class__.creative3 = creatives[2]

    if not self.__class__.line_item_id:
      filter_statement = {'query': 'ORDER BY name LIMIT 500'}
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      users = user_service.GetUsersByStatement(filter_statement)
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
      order_id = client.GetOrderService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateOrder(order)[0]['id']
      inventory_service = client.GetInventoryService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
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
      ad_unit_id = inventory_service.CreateAdUnit(ad_unit)[0]['id']
      line_item = {
          'name': 'Line item #%s' % Utils.GetUniqueName(),
          'orderId': order_id,
          'targeting': {
              'inventoryTargeting': {
                  'targetedAdUnitIds': [ad_unit_id]
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
      self.__class__.line_item_id = client.GetLineItemService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateLineItem(line_item)[0]['id']

  def testCreateLineItemCreativeAssociation(self):
    """Test whether we can create a line item creative association."""
    lica = {
        'creativeId': self.__class__.creative1['id'],
        'lineItemId': self.__class__.line_item_id,
        'creativeRotationType': 'EVEN'
    }
    self.assert_(isinstance(
        self.__class__.service.CreateLineItemCreativeAssociation(lica),
        tuple))

  def testCreateLineItemCreativeAssociations(self):
    """Test whether we can create a list of line item creative associations."""
    licas = [
        {
            'creativeId': self.__class__.creative2['id'],
            'lineItemId': self.__class__.line_item_id,
            'creativeRotationType': 'EVEN'
        },
        {
            'creativeId': self.__class__.creative3['id'],
            'lineItemId': self.__class__.line_item_id,
            'creativeRotationType': 'EVEN'
        }
    ]
    licas = self.__class__.service.CreateLineItemCreativeAssociations(licas)
    self.__class__.lica1 = licas[0]
    self.__class__.lica2 = licas[1]
    self.assert_(isinstance(licas, tuple))

  def testGetLineItemCreativeAssociation(self):
    """Test whether we can fetch an existing line item creative association."""
    self.assert_(isinstance(
        self.__class__.service.GetLineItemCreativeAssociation(
            self.__class__.line_item_id, self.__class__.creative2['id']),
            tuple))

  def testGetLineItemCreativeAssociationsByStatement(self):
    """Test whether we can fetch a list of existing line item creative
    associations that match given statement."""
    if not self.__class__.lica1:
      self.testCreateLineItemCreativeAssociations()
    filter_statement = {'query': 'WHERE lineItemId = \'%s\' LIMIT 500'
                        % self.__class__.line_item_id}
    self.assert_(isinstance(
        self.__class__.service.GetLineItemCreativeAssociationsByStatement(
            filter_statement),
        tuple))

  def testPerformLineItemCreativeAssociationAction(self):
    """Test whether we can deactivate a line item create association."""
    if not self.__class__.lica1:
      self.testCreateLineItemCreativeAssociations()
    action = {'type': 'DeactivateLineItemCreativeAssociations'}
    filter_statement = {'query': 'WHERE lineItemId = \'%s\' AND '
                        'status = \'ACTIVE\''  % self.__class__.line_item_id}
    self.assert_(isinstance(
        self.__class__.service.PerformLineItemCreativeAssociationAction(
            action, filter_statement), tuple))

  def testUpdateLineItemCreativeAssociation(self):
    """Test whether we can update a line item creative association."""
    if not self.__class__.lica1:
      self.testCreateLineItemCreativeAssociations()
    destination_url = 'http://news.google.com'
    self.__class__.lica1['destinationUrl'] = destination_url
    lica = self.__class__.service.UpdateLineItemCreativeAssociation(
        self.__class__.lica1)
    self.assert_(isinstance(lica, tuple))
    self.assertEqual(lica[0]['destinationUrl'], destination_url)

  def testUpdateLineItemCreativeAssociations(self):
    """Test whether we can update a list of line item creative associations."""
    if not self.__class__.lica1 or not self.__class__.lica2:
      self.testCreateLineItemCreativeAssociations()
    destination_url = 'http://news.google.com'
    self.__class__.lica1['destinationUrl'] = destination_url
    self.__class__.lica2['destinationUrl'] = destination_url
    licas = self.__class__.service.UpdateLineItemCreativeAssociations(
        [self.__class__.lica1, self.__class__.lica2])
    self.assert_(isinstance(licas, tuple))
    for lica in licas:
      self.assertEqual(lica['destinationUrl'], destination_url)


class LicaServiceTestV201010(unittest.TestCase):

  """Unittest suite for LineItemCreativeAssociationService using V201010."""

  SERVER = SERVER_V201010
  VERSION = VERSION_V201010
  client.debug = False
  service = None
  creative1 = None
  creative2 = None
  creative3 = None
  line_item_id = None
  IMAGE_DATA = open(os.path.join('data', 'medium_rectangle.jpg').replace(
      '\\', '/'), 'r').read()
  if client.soap_lib == SOAPPY:
    IMAGE_DATA = base64.encodestring(IMAGE_DATA)
  lica1 = None
  lica2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetLineItemCreativeAssociationService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (not self.__class__.creative1 or not self.__class__.creative2 or
        not self.__class__.creative3):
      company = {
        'name': 'Company #%s' % Utils.GetUniqueName(),
        'type': 'ADVERTISER'
      }
      advertiser_id = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCompany(company)[0]['id']
      creatives = []
      for i in xrange(3):
        creatives.append({
            'type': 'ImageCreative',
            'name': 'Image Creative #%s' % Utils.GetUniqueName(),
            'advertiserId': advertiser_id,
            'destinationUrl': 'http://google.com',
            'imageName': 'image.jpg',
            'imageByteArray': self.__class__.IMAGE_DATA,
            'size': {'width': '300', 'height': '250'}
        })
      creatives = client.GetCreativeService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCreatives(creatives)
      self.__class__.creative1 = creatives[0]
      self.__class__.creative2 = creatives[1]
      self.__class__.creative3 = creatives[2]

    if not self.__class__.line_item_id:
      filter_statement = {'query': 'ORDER BY name LIMIT 500'}
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      users = user_service.GetUsersByStatement(filter_statement)
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
      order_id = client.GetOrderService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateOrder(order)[0]['id']
      inventory_service = client.GetInventoryService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
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
      ad_unit_id = inventory_service.CreateAdUnit(ad_unit)[0]['id']
      line_item = {
          'name': 'Line item #%s' % Utils.GetUniqueName(),
          'orderId': order_id,
          'targeting': {
              'inventoryTargeting': {
                  'targetedAdUnitIds': [ad_unit_id]
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
      self.__class__.line_item_id = client.GetLineItemService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateLineItem(line_item)[0]['id']

  def testCreateLineItemCreativeAssociation(self):
    """Test whether we can create a line item creative association."""
    lica = {
        'creativeId': self.__class__.creative1['id'],
        'lineItemId': self.__class__.line_item_id,
        'creativeRotationType': 'EVEN'
    }
    self.assert_(isinstance(
        self.__class__.service.CreateLineItemCreativeAssociation(lica),
        tuple))

  def testCreateLineItemCreativeAssociations(self):
    """Test whether we can create a list of line item creative associations."""
    licas = [
        {
            'creativeId': self.__class__.creative2['id'],
            'lineItemId': self.__class__.line_item_id,
            'creativeRotationType': 'EVEN'
        },
        {
            'creativeId': self.__class__.creative3['id'],
            'lineItemId': self.__class__.line_item_id,
            'creativeRotationType': 'EVEN'
        }
    ]
    licas = self.__class__.service.CreateLineItemCreativeAssociations(licas)
    self.__class__.lica1 = licas[0]
    self.__class__.lica2 = licas[1]
    self.assert_(isinstance(licas, tuple))

  def testGetLineItemCreativeAssociation(self):
    """Test whether we can fetch an existing line item creative association."""
    self.assert_(isinstance(
        self.__class__.service.GetLineItemCreativeAssociation(
            self.__class__.line_item_id, self.__class__.creative2['id']),
            tuple))

  def testGetLineItemCreativeAssociationsByStatement(self):
    """Test whether we can fetch a list of existing line item creative
    associations that match given statement."""
    if not self.__class__.lica1:
      self.testCreateLineItemCreativeAssociations()
    filter_statement = {'query': 'WHERE lineItemId = \'%s\' LIMIT 500'
                        % self.__class__.line_item_id}
    self.assert_(isinstance(
        self.__class__.service.GetLineItemCreativeAssociationsByStatement(
            filter_statement),
        tuple))

  def testPerformLineItemCreativeAssociationAction(self):
    """Test whether we can deactivate a line item create association."""
    if not self.__class__.lica1:
      self.testCreateLineItemCreativeAssociations()
    action = {'type': 'DeactivateLineItemCreativeAssociations'}
    filter_statement = {'query': 'WHERE lineItemId = \'%s\' AND '
                        'status = \'ACTIVE\''  % self.__class__.line_item_id}
    self.assert_(isinstance(
        self.__class__.service.PerformLineItemCreativeAssociationAction(
            action, filter_statement), tuple))

  def testUpdateLineItemCreativeAssociation(self):
    """Test whether we can update a line item creative association."""
    if not self.__class__.lica1:
      self.testCreateLineItemCreativeAssociations()
    destination_url = 'http://news.google.com'
    self.__class__.lica1['destinationUrl'] = destination_url
    lica = self.__class__.service.UpdateLineItemCreativeAssociation(
        self.__class__.lica1)
    self.assert_(isinstance(lica, tuple))
    self.assertEqual(lica[0]['destinationUrl'], destination_url)

  def testUpdateLineItemCreativeAssociations(self):
    """Test whether we can update a list of line item creative associations."""
    if not self.__class__.lica1 or not self.__class__.lica2:
      self.testCreateLineItemCreativeAssociations()
    destination_url = 'http://news.google.com'
    self.__class__.lica1['destinationUrl'] = destination_url
    self.__class__.lica2['destinationUrl'] = destination_url
    licas = self.__class__.service.UpdateLineItemCreativeAssociations(
        [self.__class__.lica1, self.__class__.lica2])
    self.assert_(isinstance(licas, tuple))
    for lica in licas:
      self.assertEqual(lica['destinationUrl'], destination_url)


def makeTestSuiteV201004():
  """Set up test suite using V201004.

  Returns:
    TestSuite test suite using V201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LicaServiceTestV201004))
  return suite


def makeTestSuiteV201010():
  """Set up test suite using V201010.

  Returns:
    TestSuite test suite using V201010.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LicaServiceTestV201010))
  return suite


if __name__ == '__main__':
  suite_V201004 = makeTestSuiteV201004()
  suite_V201010 = makeTestSuiteV201010()
  alltests = unittest.TestSuite([suite_V201004, suite_V201010])
  unittest.main(defaultTest='alltests')
