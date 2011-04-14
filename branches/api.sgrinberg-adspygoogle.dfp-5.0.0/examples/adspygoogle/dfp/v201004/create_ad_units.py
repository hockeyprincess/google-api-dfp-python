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

"""This code example creates new ad units under a previously created ad unit. To
determine which ad units exist, run get_ad_unin_tree.py or
get_all_ad_units.py"""

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
inventory_service = client.GetInventoryService(
    'https://sandbox.google.com', 'v201004')
network_service = client.GetNetworkService(
    'https://sandbox.google.com', 'v201004')

# Set the parent ad unit's id for all ad units to be created under.
effective_root_ad_unit_id = \
    network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']

# Create ad unit objects.
ad_units = []
for i in xrange(5):
  ad_unit = {
      'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
      'parentId': effective_root_ad_unit_id,
      'description': 'Ad unit description.',
      'targetWindow': 'BLANK',
      'sizes': [{'width': '300', 'height': '250'}]
  }
  ad_units.append(ad_unit)

# Add ad units.
# The initialization of the service and addition of ad units can be
# combined into a single statement. Ex:
# ad_units = client.GetInventoryService().CreateAdUnits(ad_units)
ad_units = inventory_service.CreateAdUnits(ad_units)

# Display results.
for ad_unit in ad_units:
  print ('Ad unit with id \'%s\' was created under parent with id \'%s\'.'
         % (ad_unit['id'], effective_root_ad_unit_id))
