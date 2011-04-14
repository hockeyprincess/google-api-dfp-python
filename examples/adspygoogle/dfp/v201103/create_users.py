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

"""This code example creates new users. To determine which users exist, run
get_all_users.py"""

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
# sandbox environment.
user_service = client.GetUserService(
    'https://sandbox.google.com', 'v201103')

# Create user objects.
users = [
    {
        'email': 'INSERT_EMAIL_ADDRESS_HERE',
        'name': 'INSERT_NAME_HERE',
        'preferredLocale': 'en_US'
    },
    {
        'email': 'INSERT_ANOTHER_EMAIL_ADDRESS_HERE',
        'name': 'INSERT_ANOTHER_NAME_HERE',
        'preferredLocale': 'en_US'
    }
]
for user in users:
  user['roleId'] = 'INSERT_ROLE_ID_HERE'

# Add users.
# The initialization of the service and addition of users could've been
# combined into a single statement. Ex:
# users = client.GetUserService().CreateUsers(users)
users = user_service.CreateUsers(users)

# Display results.
for user in users:
  print ('User with id \'%s\', email \'%s\', and role \'%s\' was created.'
         % (user['id'], user['email'], user['roleName']))
