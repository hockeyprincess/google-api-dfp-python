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

"""This code example gets a forecast for a prospective line item. To determine
which orders exist, run get_all_orders.py. To determine which placements exist,
run get_all_placements.py."""

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
client.strict = False

# Initialize appropriate service. By default, the request is always made against
# the sandbox environment.
forecast_service = client.GetForecastService(
    'https://sandbox.google.com', 'v201103')

# Set the placement that the prospective line item will target.
target_placement_ids = ['INSERT_PLACEMENT_ID_HERE']

# Create prospective line item.
line_item = {
    'targeting': {
        'inventoryTargeting': {
            'targetedPlacementIds': target_placement_ids
        }
    },
    'creativeSizes': [
        {'width': '300', 'height': '250'}
    ],
    'lineItemType': 'SPONSORSHIP',
    'startDateTimeType': 'IMMEDIATELY',
    'endDateTime': {
        'date': {
            'year': '2010',
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
    'unitsBought': '50',
    'unitType': 'IMPRESSIONS'
}

# Get forecast.
forecast = forecast_service.GetForecast(line_item)[0]
matched = long(forecast['matchedUnits'])
available_percent = (long(forecast['availableUnits'])/(matched * 1.0)) * 100

# Display results.
print ('%s %s matched.\n%s%% %s available.'
       % (matched, forecast['unitType'].lower(),
          available_percent, forecast['unitType'].lower()))

if 'possibleUnits' in forecast:
  possible_percent = (long(forecast['possibleUnits'])/(matched * 1.0)) * 100
  print '%s%% %s possible' % (possible_percent, forecast['unitType'])
