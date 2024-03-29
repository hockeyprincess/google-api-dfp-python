#!/usr/bin/python
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

"""This code example creates new line items. To determine which line items
exist, run get_all_line_items.py. To determine which orders exist, run
get_all_orders.py. To determine which placements exist, run
get_all_placements.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.common import Utils
from adspygoogle.dfp.DfpClient import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service. By default, the request is always made against
# sandbox environment.
line_item_service = client.GetLineItemService(
    'https://sandbox.google.com', 'v201103')

# Set order that all created line items will belong to and the placement id to
# target.
order_id = 'INSERT_LINE_ITEM_ID_HERE'
targeted_placement_ids = ['INSERT_PLACEMENT_ID_HERE']

# Create line item objects.
line_items = []
for i in xrange(5):
  line_item = {
      'name': 'Line item #%s' % Utils.GetUniqueName(),
      'orderId': order_id,
      'targeting': {
          'inventoryTargeting': {
              'targetedPlacementIds': targeted_placement_ids
          },
          'geoTargeting': {
              'targetedLocations': [
                  {
                      'xsi_type': 'CountryLocation',
                      'countryCode': 'US'
                  },
                  {
                      'xsi_type': 'RegionLocation',
                      'regionCode': 'CA-QC'
                  }
              ],
              'excludedLocations': [
                  {
                      'xsi_type': 'CityLocation',
                      'cityName': 'Chicago',
                      'countryCode': 'US'
                  },
                  {
                      'xsi_type': 'MetroLocation',
                      'metroCode': '501'
                  }
              ]
          },
          'dayPartTargeting': {
              'dayParts': [
                  {
                      'dayOfWeek': 'SATURDAY',
                      'startTime': {
                          'hour': '0',
                          'minute': 'ZERO'
                      },
                      'endTime': {
                          'hour': '24',
                          'minute': 'ZERO'
                      }
                  },
                  {
                      'dayOfWeek': 'SUNDAY',
                      'startTime': {
                          'hour': '0',
                          'minute': 'ZERO'
                      },
                      'endTime': {
                          'hour': '24',
                          'minute': 'ZERO'
                      }
                  }
              ],
              'timeZone': 'BROWSER'
          },
          'userDomainTargeting': {
              'domains': ['usa.gov'],
              'targeted': 'false'
          }
      },
      'creativeSizes': [
          {'width': '300', 'height': '250'},
          {'width': '120', 'height': '600'}
      ],
      'startDateTimeType': 'IMMEDIATELY',
      'lineItemType': 'STANDARD',
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
  line_items.append(line_item)

# Add line items.
# The initialization of the service and addition of line items could've been
# combined into a single statement. Ex:
# line_items = client.GetLineItemService().CreateLineItems(line_items)
line_items = line_item_service.CreateLineItems(line_items)

# Display results.
for line_item in line_items:
  print ('Line item with id \'%s\', belonging to order id \'%s\', and named '
         '\'%s\' was created.' % (line_item['id'], line_item['orderId'],
                                  line_item['name']))
