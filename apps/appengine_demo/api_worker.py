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

"""Worker script to communicate with the Google's DoubleClick for Publishers API
client library."""


import os
import sys
import time

LIB_HOME = 'lib'
sys.path.append(LIB_HOME)

from adspygoogle.common import PYXML
from adspygoogle.common import ZSI
from adspygoogle.common import Utils
from adspygoogle.dfp import DfpUtils
from adspygoogle.dfp.DfpClient import DfpClient
from adspygoogle.dfp.DfpErrors import DfpError


# Enable to see debugging data in App Engine's console, when API call is made.
DEBUG = False
SOAP_LIB = ZSI
SERVER = 'https://sandbox.google.com'
VERSION = 'v201010'

DEMO_VERSION = '1.0.0'


def SetUpClient(email, password):
  """Return instance of Client.

  Args:
    email: str Login email for the Google Account.
    password: str Password for the Google Account.

  Returns:
    Client instance.
  """
  client = DfpClient(
      path='.',
      headers={
          'email': email,
          'password': password,
          'applicationName': 'AppEngine Demo v%s' % DEMO_VERSION},
      # The app engine doesn't like when data is written to disc. Thus, we need
      # to explicitly turn off logging. Though, if debugging is enabled, the
      # data from STDOUT will be redirected to app engine's debugging console.
      config={
          'debug': Utils.BoolTypeConvert(DEBUG),
          'xml_log': 'n',
          'request_log': 'n',
          'pretty_xml': 'n',
          'xml_parser': PYXML,
          'soap_lib': SOAP_LIB,
          'compress': 'n'
      })
  return client


def ReadFile(f_path):
  """Load data from a given file.

  Args:
    f_path: str Absolute path to the file to read.

  Returns:
    str Data loaded from the file, None otherwise.
  """
  return Utils.ReadFile(f_path)


def GetEntities(client, service_name, query='', filter_statement=None):
  """Get existing entities.

  Args:
    client: Instance of Client.
    service_name: str Name of the service to use.
    query: str a statement filter to apply, if any. The default is empty string.
    filter_statement: dict Publisher Query Language statement.

  Returns:
    list List of existing entities.
  """
  if not filter_statement:
    return DfpUtils.GetAllEntitiesByStatement(client, service_name, query)
  elif service_name == 'Order':
    service = client.GetOrderService(SERVER, VERSION)
    return service.GetOrdersByStatement(filter_statement)
  elif service_name == 'LineItem':
    service = client.GetLineItemService(SERVER, VERSION)
    return service.GetLineItemsByStatement(filter_statement)
  elif service_name == 'Inventory':
    service = client.GetInventoryService(SERVER, VERSION)
    return service.GetAdUnitsByStatement(filter_statement)


def CreateAdvertisers(client):
  """Create new advertisers.

  Args:
    client: Instance of client.

  Returns:
    list List of new advertisers.
  """
  company_service = client.GetCompanyService()
  companies = [
      {
          'name': 'Google Inc.',
          'type': 'ADVERTISER'
      },
      {
          'name': 'Famous Shoe Company',
          'type': 'ADVERTISER'
      },
      {
          'name': 'Happy Trails',
          'type': 'ADVERTISER'
      }
  ]
  companies = company_service.CreateCompanies(companies)
  return companies


def CreateOrder(client, name, advertiser_id, salesperson_id, trafficker_id):
  """Create an order for a given advertiser, salesperson, and trafficker.

  Args:
    client: Instance of client.
    name: str Name of the order.
    advertiser_id: str Id of existing advertiser.
    salesperson_id: str Id of existing salesperson.
    trafficker_id: str Id of existing trafficker.

  Returns:
    dict New order.
  """
  order_service = client.GetOrderService(SERVER, VERSION)
  order = {
    'name': name,
    'advertiserId': advertiser_id,
    'salespersonId': salesperson_id,
    'traffickerId': trafficker_id
  }
  order = order_service.CreateOrder(order)[0]
  return order


def CreateCreatives(client, advertiser_id):
  """Create new creatives for a given advertiser id.

  Args:
    client: Instance of client.
    advertiser_id: str Advertiser id.

  Returns:
    list List of new creatives.
  """
  creative_service = client.GetCreativeService(SERVER, VERSION)
  new_creatives = [
      {
          'type': 'ImageCreative',
          'name': 'Image Creative #%s' % str(time.time()).split('.')[0],
          'advertiserId': advertiser_id,
          'destinationUrl': 'http://google.com',
          'imageName': 'medium_rectangle.jpg',
          'imageByteArray': open(os.path.join(os.getcwd(), 'data',
              'inline.jpg').replace('\\', '/'), 'r').read(),
          'size': {'width': '300', 'height': '250'}
      },
      {
          'type': 'ImageCreative',
          'name': 'Image Creative #%s' % str(time.time()).split('.')[0],
          'advertiserId': advertiser_id,
          'destinationUrl': 'http://google.com',
          'imageName': 'skyscraper.jpg',
          'imageByteArray': open(os.path.join(os.getcwd(), 'data',
              'skyscraper.jpg').replace('\\', '/'), 'r').read(),
          'size': {'width': '120', 'height': '600'}
      }
  ]
  creatives = []
  for creative in new_creatives:
    creatives.append(creative_service.CreateCreative(creative)[0])
  return creatives


def CreateLineItem(client, order_id, line_item):
  """Create new line item for a given order.

  Args:
    client: Instance of client.
    order_id: str Order id.
    line_item: dict Line item to create.
  """
  placement_service = client.GetPlacementService(SERVER, VERSION)
  line_item_service = client.GetLineItemService(SERVER, VERSION)
  network_service = client.GetNetworkService(SERVER, VERSION)
  inventory_service = client.GetInventoryService(SERVER, VERSION)

  medium_rectangle_ad_unit_placement = {
    'name': 'Medium rectangle AdUnit Placement #%s' % Utils.GetUniqueName(),
    'description': 'Contains ad units that can hold creatives of size 300x250',
    'targetedAdUnitIds': []
  }
  skyscraper_ad_unit_placement = {
      'name': 'Skyscraper AdUnit Placement #%s' % Utils.GetUniqueName(),
      'description': ('Contains ad units that can hold creatives of size '
                      '120x600'),
      'targetedAdUnitIds': []
  }
  banner_ad_unit_placement = {
      'name': 'Banner AdUnit Placement #%s' % Utils.GetUniqueName(),
      'description': 'Contains ad units that can hold creatives of size 468x60',
      'targetedAdUnitIds': []
  }
  ad_units = GetEntities(client, 'Inventory', '',
                         {'query': 'LIMIT 500'})[0]['results']

  # Upload 1 ad unit, if none were found.
  if not ad_units:
    ad_units = [
        {
            'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
            'description': 'Ad unit description.',
            'targetWindow': 'BLANK',
            'sizes': [{'width': '300', 'height': '250'}]
        },
        {
            'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
            'description': 'Ad unit description.',
            'targetWindow': 'BLANK',
            'sizes': [{'width': '120', 'height': '600'}]
        },
        {
            'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
            'description': 'Ad unit description.',
            'targetWindow': 'BLANK',
            'sizes': [{'width': '468', 'height': '60'}]
        }
    ]
    ad_units = inventory_service.CreateAdUnits(ad_units)

  # Separate the ad units by size.
  for ad_unit in ad_units:
    for size in ad_unit['sizes']:
      if size['width'] == '300' and size['height'] == '250':
        medium_rectangle_ad_unit_placement['targetedAdUnitIds'].append(
            ad_unit['id'])
      elif size['width'] == '120' and size['height'] == '600':
        skyscraper_ad_unit_placement['targetedAdUnitIds'].append(ad_unit['id'])
      elif size['width'] == '468' and size['height'] == '60':
        banner_ad_unit_placement['targetedAdUnitIds'].append(ad_unit['id'])

  placements = placement_service.CreatePlacements(
      [medium_rectangle_ad_unit_placement, skyscraper_ad_unit_placement,
       banner_ad_unit_placement])
  placement_ids = [placement['id'] for placement in placements]

  currency_code = network_service.GetCurrentNetwork()[0]['currencyCode']

  new_line_item = {
      'name': line_item['name'],
      'orderId': order_id,
      'targeting': {
          'inventoryTargeting': {
              'targetedPlacementIds': placement_ids
          }
      },
      'creativeSizes': [
          {'width': '300', 'height': '250'},
          {'width': '120', 'height': '600'}
      ],
      'startType': 'IMMEDIATELY',
      'lineItemType': line_item['lineItemType'],
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
          'currencyCode': currency_code,
          'microAmount': line_item['microAmount']
      },
      'creativeRotationType': 'EVEN',
      'discountType': 'PERCENTAGE',
      'unitsBought': line_item['unitsBought'],
      'unitType': line_item['unitType']
  }
  line_item_service.CreateLineItem(new_line_item)


def UpdateLineItem(client, order_id, new_line_item):
  """Update an existing line item.

  Args:
    client: Instance of client.
    order_id: str Order id.
    new_line_item: dict New data values for line item.
  """
  line_item_service = client.GetLineItemService(SERVER, VERSION)
  line_item = line_item_service.GetLineItem(new_line_item['id'])[0]

  # Update line item fields.
  line_item['name'] = new_line_item['name']
  line_item['lineItemType'] = new_line_item['lineItemType']
  line_item['costPerUnit']['microAmount'] = new_line_item['microAmount']
  line_item['unitsBought'] = new_line_item['unitsBought']
  line_item['unitType'] = new_line_item['unitType']
  line_item_service.UpdateLineItem(line_item)


def CreateLica(client, creative_id, line_item_id):
  """Create a line item creative association for given creative and line item
  ids.

  Args:
    client: Instance of client.
    creative_id: str Creative id.
    line_item_id: str Line item id.

  Returns:
    dict New lica.
  """
  lica_service = client.GetLineItemCreativeAssociationService(SERVER, VERSION)
  lica = {
      'creativeId': creative_id,
      'lineItemId': line_item_id
  }
  lica = lica_service.CreateLineItemCreativeAssociation(lica)[0]
  return lica
