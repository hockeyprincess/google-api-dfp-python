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

"""This code example updates the delivery rate of all line items up to the first
500. To determine which line items exist, run get_all_line_items.py."""

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
# the sandbox environment.
line_item_service = client.GetLineItemService(
    'https://sandbox.google.com', 'v201010')

# Set id of the order to get line items from.
order_id = 'INSERT_ORDER_ID_HERE'

# Create statement object to only select line items with even delivery rates.
filter_statement = {'query': 'WHERE deliveryRateType = \'EVENLY\' and '
                             'orderId = \'%s\' LIMIT 500' % order_id}

# Get line items by statement.
line_items = line_item_service.GetLineItemsByStatement(
    filter_statement)[0]['results']

if line_items:
  # Update each local line item by changing its delivery rate type.
  updated_line_items = []
  for line_item in line_items:
    if not Utils.BoolTypeConvert(line_item['isArchived']):
      line_item['deliveryRateType'] = 'AS_FAST_AS_POSSIBLE'
      updated_line_items.append(line_item)

  # Update line items remotely.
  line_items = line_item_service.UpdateLineItems(updated_line_items)

  # Display results.
  if line_items:
    for line_item in line_items:
      print ('Line item with id \'%s\', belonging to order id \'%s\', named '
         '\'%s\', and delivery rate \'%s\' was updated.'
         % (line_item['id'], line_item['orderId'], line_item['name'],
            line_item['deliveryRateType']))
  else:
    print 'No line items were updated.'
else:
  print 'No companies found to update.'
