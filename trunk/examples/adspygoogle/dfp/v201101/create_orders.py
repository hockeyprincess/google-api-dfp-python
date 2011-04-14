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

"""This code example creates new orders. To determine which orders exist, run
get_all_orders.py."""

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
order_service = client.GetOrderService(
    'https://sandbox.google.com', 'v201101')

# Set advertiser (company), salesperson, and trafficker to assign to each order.
advertiser_id = 'INSERT_ADVERTISER_COMPANY_ID_HERE'
salesperson_id = 'INSERT_SALESPERSON_ID_HERE'
trafficker_id = 'INSERT_TRAFFICKER_ID_HERE'

# Create order objects.
orders = []
for i in xrange(5):
  order = {
      'name': 'Order #%s' % Utils.GetUniqueName(),
      'advertiserId': advertiser_id,
      'salespersonId': salesperson_id,
      'traffickerId': trafficker_id
  }
  orders.append(order)

# Add orders.
# The initialization of the service and addition of orders could've been
# combined into a single statement. Ex:
# orders = client.GetOrderService().CreateOrders(orders)
orders = order_service.CreateOrders(orders)

# Display results.
for order in orders:
  print ('Order with id \'%s\' and name \'%s\' was created.'
         % (order['id'], order['name']))
