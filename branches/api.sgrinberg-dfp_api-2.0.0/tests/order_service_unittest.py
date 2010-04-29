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

"""Unit tests to cover OrderService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import time
import unittest

from tests import HTTP_PROXY
from tests import SERVER
from tests import client


class OrderServiceTestV201002(unittest.TestCase):

  """Unittest suite for OrderService using v201002."""

  SERVER_V201002 = SERVER
  VERSION_V201002 = 'v201002'
  client.debug = False
  service = None
  advertiser_id = '0'
  salesperson_id = '0'
  trafficker_id = '0'
  order1 = None
  order2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetOrderService(
          self.__class__.SERVER_V201002, self.__class__.VERSION_V201002,
          HTTP_PROXY)

    if self.__class__.advertiser_id is '0':
      company = {
        'name': 'Company #%s' % time.time(),
        'type': 'ADVERTISER'
      }
      self.__class__.advertiser_id = client.GetCompanyService(
          self.__class__.SERVER_V201002,
          self.__class__.VERSION_V201002,
          HTTP_PROXY).CreateCompany(company)[0]['id']

    if self.__class__.trafficker_id is '0':
      filter = {'text': 'ORDER BY name LIMIT 500'}
      users = client.GetUserService(
          self.__class__.SERVER_V201002, self.__class__.VERSION_V201002,
          HTTP_PROXY).GetUsersByFilter(filter)
      for user in users[0]['results']:
        if user['roleName'] in ('Salesperson',):
          self.__class__.salesperson_id = user['id']
          continue
        elif user['roleName'] in ('Trafficker',):
          self.__class__.trafficker_id = user['id']
          continue

  def testCreateOrder(self):
    """Test whether we can create an order."""
    order = {
        'advertiserId': self.__class__.advertiser_id,
        'currencyCode': 'USD',
        'name': 'Order #%s' % time.time(),
        'traffickerId': self.__class__.trafficker_id
    }
    self.assert_(isinstance(
        self.__class__.service.CreateOrder(order), tuple))

  def testCreateOrders(self):
    """Test whether we can create a list of orders."""
    orders = [
        {
            'advertiserId': self.__class__.advertiser_id,
            'currencyCode': 'USD',
            'name': 'Order #%s' % time.time(),
            'traffickerId': self.__class__.trafficker_id
        },
        {
            'advertiserId': self.__class__.advertiser_id,
            'currencyCode': 'USD',
            'name': 'Order #%s' % str(time.time()) + '0.01',
            'traffickerId': self.__class__.trafficker_id
        }
    ]
    orders = self.__class__.service.CreateOrders(orders)
    self.__class__.order1 = orders[0]
    self.__class__.order2 = orders[1]
    self.assert_(isinstance(orders, tuple))

  def testGetOrder(self):
    """Test whether we can fetch an existing order."""
    if not self.__class__.order1:
      self.testCreateOrders()
    self.assert_(isinstance(self.__class__.service.GetOrder(
        self.__class__.order1['id']), tuple))

  def testGetOrdersByFilter(self):
    """Test whether we can fetch a list of existing orders that match given
    filter."""
    filter = {'text': 'WHERE advertiserId = \'%s\' LIMIT 500'
                      % self.__class__.advertiser_id}
    self.assert_(isinstance(self.__class__.service.GetOrdersByFilter(filter),
                            tuple))

  def testPerformOrderAction(self):
    """Test whether we can approve order."""
    action = {'type': 'ApproveOrders'}
    filter = {'text': 'WHERE status = \'DRAFT\''}
    self.assert_(isinstance(
        self.__class__.service.PerformOrderAction(action, filter), tuple))

  def testUpdateOrder(self):
    """Test whether we can update an order."""
    if not self.__class__.order1:
      self.testCreateOrders()
    notes = 'Spoke to advertiser. All is well.'
    self.__class__.order1['notes'] = notes
    order = self.__class__.service.UpdateOrder(self.__class__.order1)
    self.assert_(isinstance(order, tuple))
    self.assertEqual(order[0]['notes'], notes)

  def testUpdateOrders(self):
    """Test whether we can update a list of orders."""
    if not self.__class__.order1 or not self.__class__.order2:
      self.testCreateOrders()
    notes = 'Spoke to advertiser. All is well.'
    self.__class__.order1['notes'] = notes
    self.__class__.order2['notes'] = notes
    orders = self.__class__.service.UpdateOrders([self.__class__.order1,
                                                  self.__class__.order2])
    self.assert_(isinstance(orders, tuple))
    for order in orders:
      self.assertEqual(order['notes'], notes)


def makeTestSuiteV201002():
  """Set up test suite using v201002.

  Returns:
    TestSuite test suite using v201002.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(OrderServiceTestV201002))
  return suite


if __name__ == '__main__':
  suite_v201002 = makeTestSuiteV201002()
  alltests = unittest.TestSuite([suite_v201002])
  unittest.main(defaultTest='alltests')
