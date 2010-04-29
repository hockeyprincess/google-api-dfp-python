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

"""This code example creates new line item creative associations (LICAs) from
a given creative and existing line items belonging to an order. To determine
which creatives exist, run get_all_creatives.py. To determine which orders
exist, run get_all_orders.py. To determine which LICAs exist, run
get_all_licas.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import sys
sys.path.append('../..')

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
lica_service = client.GetLineItemCreativeAssociationService()

# Set order to get line items from and the creative to associate them with.
order_id = 'INSERT_ORDER_ID_HERE'
creative_id = 'INSERT_CREATIVE_ID_HERE'

# Create filter object to get first 500 items for the given order. To get more
# than 500 line items, see get_all_line_items.py.
filter = {'text': 'WHERE orderId = \'%s\' LIMIT 500' % order_id}

# Get line items by filter.
line_items = line_item_service.GetLineItemsByFilter(filter)[0]['results']

if line_items:
  # Create LICA objects.
  licas = []
  for line_item in line_items:
    lica = {
        'creativeId': creative_id,
        'lineItemId': line_item['id'],
        'status': 'ACTIVE'
    }
    licas.append(lica)

    # Create the LICAs remotely.
    licas = lica_service.CreateLineItemCreativeAssociations(licas)

    # Display results.
    if licas:
      for lica in licas:
        print ('LICA with line item id \'%s\', creative id \'%s\', and '
               'status \'%s\' was created.' % (lica['id'], lica['creativeId'],
                                               lica['status']))
    else:
      print 'No LICAs created.'
else:
  print 'No line items to associate the creative with.'
