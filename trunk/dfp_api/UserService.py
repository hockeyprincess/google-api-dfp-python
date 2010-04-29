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

"""Methods to access UserService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from dfp_api import SanityCheck as glob_sanity_check
from dfp_api.Errors import ValidationError
from dfp_api.WebService import WebService


class UserService(object):

  """Wrapper for UserService.

  The User Service provides operations for creating, updating and retrieving
  users.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits UserService.

    Args:
      headers: dict dictionary object with populated authentication
               credentials.
      config: dict dictionary object with populated configuration values.
      op_config: dict dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock the thread lock
      logger: Logger the instance of Logger
    """
    url = [op_config['server'], 'apis/ads/publisher', op_config['version'],
           self.__class__.__name__]
    self.__service = WebService(headers, config, op_config, '/'.join(url), lock,
                                logger)
    self.__config = config
    from dfp_api import API_VERSIONS
    from dfp_api.zsi_toolkit import SanityCheck
    if op_config['version'] in API_VERSIONS:
      web_services = __import__('dfp_api.zsi_toolkit.%s.%s_services'
                                % (op_config['version'],
                                   self.__class__.__name__), globals(),
                                locals(), [''])
    else:
      msg = 'Invalid API version, not one of %s.' % str(list(API_VERSIONS))
      raise ValidationError(msg)
    self._web_services = web_services
    self.__loc = eval('web_services.%sLocator()' % self.__class__.__name__)
    self.__sanity_check = SanityCheck

  def CreateUser(self, user):
    """Create a new user.

    Args:
      user: dict a user to create.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateUser(user)

    method_name = 'createUser'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'user': user},)), 'User',
                                     self.__loc, request)

  def CreateUsers(self, users):
    """Create a list of new users.

    Args:
      users: list the users to create.

    Returns:
      tuple The response from the API method.
    """
    glob_sanity_check.ValidateTypes(((users, list),))
    for item in users:
      self.__sanity_check.ValidateUser(item)

    method_name = 'createUsers'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'users': users},)),
                                     'User', self.__loc, request)

  def GetAllRoles(self):
    """Return the roles that exist within the given network.

    Returns:
      tuple response from the API method.
    """
    method_name = 'getAllRoles'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (), 'User', self.__loc,
                                     request)

  def GetUser(self, user_id):
    """Return the user uniquely identified by the given id.

    Args:
      user_id: str ID of the user, which must already exist.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((user_id, (str, unicode)),))

    method_name = 'getUser'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'userId': user_id},)),
                                     'User', self.__loc, request)

  def GetUsersByStatement(self, filter_statement):
    """Return the users that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple response from the API method.
    """
    filter_statement = self.__sanity_check.ValidateStatement(filter_statement,
                                                             self._web_services)

    method_name = 'getUsersByStatement'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'filterStatement': filter_statement},)),
                                     'User', self.__loc, request)

  def PerformUserAction(self, action, filter_statement):
    """Perform action on users that match the given statement.

    Args:
      action: dict the action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple response from the API method.
    """
    action = self.__sanity_check.ValidateAction(action, self._web_services)
    filter_statement = self.__sanity_check.ValidateStatement(filter_statement,
                                                             self._web_services)

    method_name = 'performUserAction'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'userAction': action},
                                       {'filterStatement': filter_statement})),
                                     'User', self.__loc, request)

  def UpdateUser(self, user):
    """Update the specified user.

    Args:
      user: dict a user to update.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateUser(user)

    method_name = 'updateUser'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'user': user},)), 'User',
                                     self.__loc, request)

  def UpdateUsers(self, users):
    """Update a list of specified users.

    Args:
      users: list the users to update.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((users, list),))
    for item in users:
      self.__sanity_check.ValidateUser(item)

    method_name = 'updateUsers'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'users': users},)),
                                     'User', self.__loc, request)
