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

"""This code example gets a forecast for an existing line item. To determine
which ine items exist, run get_all_line_items.py."""

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
forecast_service = client.GetForecastService()

# Set the line item to get a forecast for.
line_item_id = 'INSERT_LINE_ITEM_ID'

# Get forecast for line item.
forecast = forecast_service.GetForecastById(line_item_id)[0]
matched = long(forecast['forecastUnits'])
possible_percent = (long(forecast['possibleUnits'])/(matched * 1.0)) * 100
available_percent = (long(forecast['availableUnits'])/(matched * 1.0)) * 100

# Display results.
print ('%s %s matched.\n%s%% %s possible.\n%s%% %s available.'
       % (matched, forecast['unitType'].lower(),
          possible_percent, forecast['unitType'].lower(),
          available_percent, forecast['unitType'].lower()))
