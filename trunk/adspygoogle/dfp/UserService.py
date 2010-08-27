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

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp.DfpWebService import DfpWebService


class UserService(ApiService):

  """Wrapper for UserService.

  The User Service provides operations for creating, updating and retrieving
  users.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits UserService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], 'apis/ads/publisher', op_config['version'],
           self.__class__.__name__]
    self.__service = DfpWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(UserService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateUser(self, user):
    """Create a new user.

    Args:
      user: dict User to create.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateUser(user)

    method_name = 'createUser'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      user = self._message_handler.PackDictAsXml(user, 'user',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (user))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'user': user},)), 'User',
                                       self._loc, request)

  def CreateUsers(self, users):
    """Create a list of new users.

    Args:
      users: list Users to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((users, list),))
    for item in users:
      self._sanity_check.ValidateUser(item)

    method_name = 'createUsers'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      new_users = []
      for user in users:
        new_users.append(self._message_handler.PackDictAsXml(user, 'users',
            OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_users)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'users': users},)),
                                       'User', self._loc, request)

  def GetAllRoles(self):
    """Return the roles that exist within the given network.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getAllRoles'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'User', self._loc,
                                       request)

  def GetUser(self, user_id):
    """Return the user uniquely identified by the given id.

    Args:
      user_id: str ID of the user, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((user_id, (str, unicode)),))

    method_name = 'getUser'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      user_id = self._message_handler.PackDictAsXml(user_id, 'userId',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (user_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'userId': user_id},)),
                                       'User', self._loc, request)

  def GetUsersByStatement(self, filter_statement):
    """Return the users that match the given filter.

    Args:
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getUsersByStatement'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      filter_statement = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateStatement(filter_statement),
          'filterStatement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (filter_statement))
    elif self._config['soap_lib'] == ZSI:
      filter_statement = self._sanity_check.ValidateStatement(
          filter_statement, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
          (({'filterStatement': filter_statement},)), 'User', self._loc,
          request)

  def PerformUserAction(self, action, filter_statement):
    """Perform action on users that match the given filter.

    Args:
      action: str Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'performUserAction'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      self._sanity_check.ValidateAction(action)
      action = self._message_handler.PackDictAsXml(action, 'userAction',
          OBJ_KEY_ORDER_MAP)
      filter_statement = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateStatement(filter_statement),
          'filterStatement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name,
                                       (''.join([action, filter_statement])))
    elif self._config['soap_lib'] == ZSI:
      action = self._sanity_check.ValidateAction(action, self._web_services)
      filter_statement = self._sanity_check.ValidateStatement(
          filter_statement, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
          (({'userAction': action}, {'filterStatement': filter_statement})),
          'User', self._loc, request)

  def UpdateUser(self, user):
    """Update the specified user.

    Args:
      user: dict User to update.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateUser(user)

    method_name = 'updateUser'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      user = self._message_handler.PackDictAsXml(user, 'user',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (user))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'user': user},)), 'User',
                                       self._loc, request)

  def UpdateUsers(self, users):
    """Update a list of specified users.

    Args:
      users: list Users to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((users, list),))
    for item in users:
      self._sanity_check.ValidateUser(item)

    method_name = 'updateUsers'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      new_users = []
      for user in users:
        new_users.append(self._message_handler.PackDictAsXml(user, 'users',
            OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_users)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'users': users},)),
                                       'User', self._loc, request)
