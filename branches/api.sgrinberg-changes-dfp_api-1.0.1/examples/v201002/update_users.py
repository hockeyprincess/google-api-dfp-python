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

"""This code example updates all users by adding " Sr." to the end of each
name. To determine which users exist, run get_all_users.py."""

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
user_service = client.GetUserService()

# Create filter object to get all users.
filter = {'text': 'LIMIT 500'}

# Get users by filter.
users = user_service.GetUsersByFilter(filter)[0]['results']

if users:
  # Update each local user object by appending ' Sr.' to its name.
  for user in users:
    user['name'] += ' Sr.'

  # Update users remotely.
  users = user_service.UpdateUsers(users)

  # Display results.
  if users:
    for user in users:
      print ('User with id \'%s\', email \'%s\', and role \'%s\' was updated.'
             % (user['id'], user['email'], user['roleName']))
  else:
    print 'No users were updated.'
else:
  print 'No users found to update.'
