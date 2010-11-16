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

"""This code example approves all draft orders. To determine which orders exist,
run get_all_orders.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfp import DfpUtils
from adspygoogle.dfp.DfpClient import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service. By default, the request is always made against
# sandbox environment.
order_service = client.GetOrderService(
    'https://sandbox.google.com', 'v201010')

# Create query.
query = 'WHERE status in (\'DRAFT\', \'PENDING_APPROVAL\')'

# Get orders by statement.
orders = DfpUtils.GetAllEntitiesByStatement(client, 'Order', query)
for order in orders:
  print ('Order with id \'%s\', name \'%s\', and status \'%s\' will be '
         'approved.' % (order['id'], order['name'], order['status']))
print 'Number of orders to be approved: %s' % len(orders)

# Perform action.
result = order_service.PerformOrderAction({'type': 'ApproveOrders'},
                                          {'query': query})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of orders approved: %s' % result['numChanges']
else:
  print 'No orders were approved.'
