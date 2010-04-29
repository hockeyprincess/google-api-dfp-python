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

"""This code example creates new line items. To determine which line items exist,
run get_all_line_items.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import sys
sys.path.append('../..')
import time

# Import appropriate classes from the client library.
from dfp_api.Client import Client


# Initialize Client object. The "path" parameter should point to the location of
# pickles, which get generated after execution of "dfp_api_config.py" script.
# The same location is used for the "logs/" directory, if logging is enabled.
client = Client(path='../..')

# Temporarily disable debugging. If enabled, the debugging data will be sent to
# STDOUT.
client.debug = False

# Initialize appropriate service. By default, the request is always made against
# sandbox environment.
line_item_service = client.GetLineItemService()

# Set order that all created line items will belong to and the ad unit id to
# target.
order_id = 'INSERT_LINE_ITEM_ID_HERE'
target_ad_unit_ids = ['INSERT_AD_UNIT_ID_HERE']

# Create line item objects.
line_items = []
for i in xrange(5):
  line_item = {
      'name': 'Line item #%s' % str(time.time()).split('.')[0] + str(i),
      'orderId': order_id,
      'targeting': {
          'inventoryTargeting': {
              'targetedAdUnitIds': target_ad_unit_ids
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
