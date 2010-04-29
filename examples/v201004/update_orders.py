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

"""This code example updates the notes of each order up to the first 500. To
determine which orders exist, run get_all_orders.py."""

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
# the sandbox environment.
order_service = client.GetOrderService()

# Create statement object to get all orders.
filter_statement = {'query': 'LIMIT 500'}

# Get orders by statement.
orders = order_service.GetOrdersByStatement(filter_statement)[0]['results']

if orders:
  # Update each local order object by changing its notes.
  for order in orders:
    order['notes'] = 'Spoke to advertiser. All is well.'

  # Update orders remotely.
  orders = order_service.UpdateOrders(orders)

  # Display results.
  if orders:
    for order in orders:
      print ('Order with id \'%s\', name \'%s\', advertiser id \'%s\', and '
             'notes \'%s\' was updated.'
             % (order['id'], order['name'], order['advertiserId'],
                order['notes']))
  else:
    print 'No orders were updated.'
else:
  print 'No orders found to update.'
