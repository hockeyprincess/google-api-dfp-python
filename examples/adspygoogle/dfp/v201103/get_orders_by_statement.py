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

"""This code example gets all orders for a given advertiser. The statement
retrieves up to the maximum page size limit of 500. To create orders, run
create_orders.py. To determine which companies are advertisers, run
get_companies_by_statement.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfp.DfpClient import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service. By default, the request is always made against
# the sandbox environment.
order_service = client.GetOrderService(
    'https://sandbox.google.com', 'v201103')

# Set id of the advertiser (company) to get orders for.
advertiser_id = 'INSERT_ADVERTISER_COMPANY_ID_HERE'

# Create statement object to get all orders for a given advertiser.
values = [{
    'key': 'advertiserId',
    'value': {
        'xsi_type': 'NumberValue',
        'value': advertiser_id
    }
}]
filter_statement = {'query': 'WHERE advertiserId = :advertiserId LIMIT 500',
                    'values': values}

# Get orders by statement.
orders = order_service.GetOrdersByStatement(filter_statement)[0]['results']

# Display results.
for order in orders:
  print ('Order with id \'%s\' name \'%s\' was found.'
         % (order['id'], order['name']))

print
print 'Number of results found: %s' % len(orders)
