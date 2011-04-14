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

"""This code example gets all users sorted by name. The statement retrieves up
to the maximum page size limit of 500. To create new users,
run create_users.py."""

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
user_service = client.GetUserService(
    'https://sandbox.google.com', 'v201101')

# Create statement object to get all users stored by name.
filter_statement = {'query': 'ORDER BY name LIMIT 500'}

# Get users by statement.
users = user_service.GetUsersByStatement(filter_statement)[0]['results']

# Display results.
for user in users:
  print ('User with id \'%s\', email \'%s\', and role \'%s\' was found.'
         % (user['id'], user['email'], user['roleName']))

print
print 'Number of results found: %s' % len(users)
