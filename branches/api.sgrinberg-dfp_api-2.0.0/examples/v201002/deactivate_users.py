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

"""This code example deactivates a user. Deactivated users can no longer make
requests to the API. The user making the request cannot deactivate itself. To
determine which users exist, run get_all_users.py."""

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
user_service = client.GetUserService()

# Set the id of the user to deactivate.
user_id = 'INSERT_USER_ID_HERE'

# Create filter.
filter = 'WHERE id = \'%s\'' % user_id

# Get users by filter.
users = Utils.GetAllEntitiesByFilter(client, 'User', filter)
for user in users:
  print ('User with id \'%s\', email \'%s\', and status \'%s\' will be '
         'deactivated.'
         % (user['id'], user['email'],
            {'true': 'ACTIVE', 'false': 'INACTIVE'}[user['isActive']]))
print 'Number of users to be deactivated: %s' % len(users)

# Perform action.
result = user_service.PerformUserAction({'type': 'DeactivateUsers'},
                                        {'text': filter})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of users deactivated: %s' % result['numChanges']
else:
  print 'No users were deactivated.'
