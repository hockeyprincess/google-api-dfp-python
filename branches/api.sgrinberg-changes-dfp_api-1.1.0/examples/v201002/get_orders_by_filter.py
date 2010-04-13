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

"""This code example gets all orders for a given advertiser. The filter
retrieves up to the maximum page size limit of 500. To create orders, run
create_orders.py."""

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

# Set id of the advertiser to get orders for.
advertiser_id = 'INSERT_ADVERTISER_ID_HERE'

# Create filter object to get all orders for a given advertiser.
filter = {'text': 'WHERE advertiserId = \'%s\' LIMIT 500' % advertiser_id}

# Get orders by filter.
orders = order_service.GetOrdersByFilter(filter)[0]['results']

# Display results.
for order in orders:
  print ('Order with id \'%s\' name \'%s\' was found.'
         % (order['id'], order['name']))

print
print 'Number of results found: %s' % len(orders)
