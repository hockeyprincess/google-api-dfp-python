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

"""This code example deactivates all active placements. To determine which
placements exist, run get_all_placements.py."""

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
placement_service = client.GetPlacementService()

# Create filter.
filter = 'WHERE status = \'ACTIVE\''

# Get placements by filter.
placements = Utils.GetAllEntitiesByFilter(client, 'Placement', filter)
for placement in placements:
  print ('Placement with id \'%s\', name \'%s\', and status \'%s\' will be '
         'deactivated.' % (placement['id'], placement['name'],
                           placement['status']))
print 'Number of placements to be deactivated: %s' % len(placements)

# Perform action.
result = placement_service.PerformPlacementAction(
    {'type': 'DeactivatePlacements'}, {'text': filter})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of placements deactivated: %s' % result['numChanges']
else:
  print 'No placements were deactivated.'