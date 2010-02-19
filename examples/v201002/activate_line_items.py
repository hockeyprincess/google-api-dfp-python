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

"""This code example activates all line items for the given order. To be
activated, line items need to be in the approved state and have at least one
creative associated with them. To approve line items, approve the order to
which they belong by running approve_orders.py. To create LICAs, run
create_licas.py. To determine which line items exist, run
get_all_line_items.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import sys
sys.path.append('../..')

# Import appropriate classes from the client library.
from dfp_api import Utils
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

# Set the id of the order to get line items from.
order_id = 'INSERT_ORDER_ID_HERE'

# Create filter.
filter = 'WHERE orderId = \'%s\' AND status = \'APPROVED\'' % order_id

# Get line items by filter.
line_items = Utils.GetAllEntitiesByFilter(client, 'LineItem', filter)
for line_item in line_items:
  print ('Line item with id \'%s\', belonging to order id \'%s\', and name '
         '\'%s\' will be activated.' % (line_item['id'], line_item['orderId'],
                                        line_item['name']))
print 'Number of line items to be activated: %s' % len(line_items)

# Perform action.
result = line_item_service.PerformLineItemAction({'type': 'ActivateLineItems'},
                                                 {'text': filter})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of line items activated: %s' % result['numChanges']
else:
  print 'No line items were activated.'
