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

"""Unit tests to cover CreativeService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append('..')
import time
import unittest

from tests import HTTP_PROXY
from tests import SERVER
from tests import client


class CreativeServiceTestV201002(unittest.TestCase):

  """Unittest suite for CreativeService using v201002."""

  SERVER_V201002 = SERVER
  VERSION_V201002 = 'v201002'
  client.debug = False
  service = None
  advertiser_id = '0'
  creative1 = None
  creative2 = None
  image_data1 = open(os.path.join(os.getcwd(), 'data',
      'medium_rectangle.jpg').replace('\\', '/'), 'r').read()
  image_data2 = open(os.path.join(os.getcwd(), 'data',
      'inline.jpg').replace('\\', '/'), 'r').read()
  image_data3 = open(os.path.join(os.getcwd(), 'data',
      'skyscraper.jpg').replace('\\', '/'), 'r').read()


  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeService(
          self.__class__.SERVER_V201002, self.__class__.VERSION_V201002,
          HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      company = {
        'name': 'Company #%s' % time.time(),
        'type': 'ADVERTISER'
      }
      company_service = client.GetCompanyService(
          self.__class__.SERVER_V201002, self.__class__.VERSION_V201002,
          HTTP_PROXY)
      self.__class__.advertiser_id = company_service.CreateCompany(
          company)[0]['id']

  def testCreateCreative(self):
    """Test whether we can create a creative."""
    creative = {
        'type': 'ImageCreative',
        'name': 'Image Creative #%s' % time.time(),
        'advertiserId': self.__class__.advertiser_id,
        'destinationUrl': 'http://google.com',
        'imageName': 'image.jpg',
        'imageByteArray': self.__class__.image_data1,
        'size': {'width': '300', 'height': '250'}
    }
    self.assert_(isinstance(
        self.__class__.service.CreateCreative(creative), tuple))

  def testCreateCreatieves(self):
    """Test whether we can create a list of creatives."""
    creatives = [
        {
            'type': 'ImageCreative',
            'name': 'Image Creative #%s' % time.time(),
            'advertiserId': self.__class__.advertiser_id,
            'destinationUrl': 'http://google.com',
            'imageName': 'inline.jpg',
            'imageByteArray': self.__class__.image_data2,
            'size': {'width': '300', 'height': '250'}
        },
        {
            'type': 'ImageCreative',
            'name': 'Image Creative #%s' % str(time.time() + 0.01),
            'advertiserId': self.__class__.advertiser_id,
            'destinationUrl': 'http://google.com',
            'imageName': 'skyscraper.jpg',
            'imageByteArray': self.__class__.image_data3,
            'size': {'width': '120', 'height': '600'}
        }
    ]
    creatives = self.__class__.service.CreateCreatives(creatives)
    self.__class__.creative1 = creatives[0]
    self.__class__.creative2= creatives[1]
    self.assert_(isinstance(creatives, tuple))

  def testGetCreative(self):
    """Test whether we can fetch an existing creative."""
    if not self.__class__.creative1:
      self.testCreateCreatieves()
    self.assert_(isinstance(self.__class__.service.GetCreative(
        self.__class__.creative1['id']), tuple))
    self.assertEqual(self.__class__.service.GetCreative(
        self.__class__.creative1['id'])[0]['Creative_Type'],
        'ImageCreative')

  def testGetCreativesByFilter(self):
    """Test whether we can fetch a list of existing creatives that match given
    filter."""
    filter = {'text': 'WHERE creativeType = \'ImageCreative\' LIMIT 500'}
    self.assert_(isinstance(
        self.__class__.service.GetCreativesByFilter(filter), tuple))

  def testUpdateCreative(self):
    """Test whether we can update a creative."""
    if not self.__class__.creative1:
      self.testCreateCreatieves()
    destination_url = 'http://news.google.com'
    image_name = 'inline.jpg'
    size = {'width': '300', 'height': '250'}
    self.__class__.creative1['destinationUrl'] = destination_url
    self.__class__.creative1['imageName'] = image_name
    self.__class__.creative1['size'] = size
    creative = self.__class__.service.UpdateCreative(self.__class__.creative1)
    self.assert_(isinstance(creative, tuple))
    self.assertEqual(creative[0]['destinationUrl'], destination_url)
    self.assertEqual(creative[0]['imageName'], image_name)
    self.assertEqual(creative[0]['size'], size)

  def testUpdateCreatives(self):
    """Test whether we can update a list of creatives."""
    if not self.__class__.creative1 or not self.__class__.creative2:
      self.testCreateCreatieves()
    destination_url = 'http://finance.google.com'
    self.__class__.creative1['destinationUrl'] = 'http://finance.google.com'
    self.__class__.creative1['imageName'] = 'inline.jpg'
    self.__class__.creative1['size'] = {'width': '300', 'height': '250'}
    self.__class__.creative2['destinationUrl'] = 'http://finance.google.com'
    self.__class__.creative2['imageName'] = 'skyscraper.jpg'
    self.__class__.creative2['size'] = {'width': '120', 'height': '600'}
    creatives = self.__class__.service.UpdateCreatives(
        [self.__class__.creative1, self.__class__.creative2])
    self.assert_(isinstance(creatives, tuple))
    for creative in creatives:
      self.assertEqual(creative['destinationUrl'], destination_url)


def makeTestSuiteV201002():
  """Set up test suite using v201002.

  Returns:
    TestSuite test suite using v201002.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CreativeServiceTestV201002))
  return suite


if __name__ == '__main__':
  suite_v201002 = makeTestSuiteV201002()
  alltests = unittest.TestSuite([suite_v201002])
  unittest.main(defaultTest='alltests')
