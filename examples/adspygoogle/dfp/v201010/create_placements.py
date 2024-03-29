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

"""This code example creates new placements for various ad unit sizes. To
determine which placements exist, run get_all_placements.py."""

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
placement_service = client.GetPlacementService(
    'https://sandbox.google.com', 'v201010')
inventory_service = client.GetInventoryService(
    'https://sandbox.google.com', 'v201010')

# Create placement object to store medium rectangle ad units.
medium_rectangle_ad_unit_placement = {
    'name': 'Medium rectangle AdUnit Placement #%s' % Utils.GetUniqueName(),
    'description': 'Contains ad units that can hold creatives of size 300x250',
    'targetedAdUnitIds': []
}

# Create placement object to store skyscraper ad units.
skyscraper_ad_unit_placement = {
    'name': 'Skyscraper AdUnit Placement #%s' % Utils.GetUniqueName(),
    'description': 'Contains ad units that can hold creatives of size 120x600',
    'targetedAdUnitIds': []
}

# Create placement object to store banner ad units.
banner_ad_unit_placement = {
    'name': 'Banner AdUnit Placement #%s' % Utils.GetUniqueName(),
    'description': 'Contains ad units that can hold creatives of size 468x60',
    'targetedAdUnitIds': []
}

# Get the first 500 ad units.
filter_statement = {'query': 'LIMIT 500'}
ad_units = inventory_service.GetAdUnitsByStatement(
    filter_statement)[0]['results']

# Separate the ad units by size.
for ad_unit in ad_units:
  for size in ad_unit['sizes']:
    if size['width'] == '300' and size['height'] == '250':
      medium_rectangle_ad_unit_placement['targetedAdUnitIds'].append(
          ad_unit['id'])
    elif size['width'] == '120' and size['height'] == '600':
      skyscraper_ad_unit_placement['targetedAdUnitIds'].append(ad_unit['id'])
    elif size['width'] == '468' and size['height'] == '60':
      banner_ad_unit_placement['targetedAdUnitIds'].append(ad_unit['id'])

# Add placements.
# The initialization of the service and addition of users could've been
# combined into a single statement. Ex:
# placements = client.GetPlacementService().CreatePlacements(
#     [medium_square_ad_unit_placement, skyscraper_ad_unit_placement,
#      banner_ad_unit_placement])
placements = placement_service.CreatePlacements(
    [medium_rectangle_ad_unit_placement, skyscraper_ad_unit_placement,
     banner_ad_unit_placement])

# Display results.
for placement in placements:
  ad_unit_ids = ''
  if 'targetedAdUnitIds' in placement:
    ad_unit_ids = ', '.join(placement['targetedAdUnitIds'])
  print ('Placement with id \'%s\', name \'%s\', and containing ad units '
         '{%s} was created.' % (placement['id'], placement['name'],
                                ad_unit_ids))
