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

"""Methods to access CreativeService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp.DfpWebService import DfpWebService
from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP


class CreativeService(ApiService):

  """Wrapper for CreativeService.

  The Creative Service provides methods for adding, updating and retrieving
  creatives.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CreativeService.

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
    super(CreativeService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateCreative(self, creative):
    """Create a new creative.

    Args:
      creative: dict Creative to create.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'createCreative'
    if self._config['soap_lib'] == SOAPPY:
      creative = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateCreative(creative), 'creative',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (creative))
    elif self._config['soap_lib'] == ZSI:
      creative = self._sanity_check.ValidateCreative(creative,
                                                     self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'creative': creative},)),
                                       'Creative', self._loc, request)

  def CreateCreatives(self, creatives):
    """Create a list of new creatives.

    Args:
      creatives: list Creatives to create.

    Returns:
      tuple response from the API method.
    """
    method_name = 'createCreatives'
    if self._config['soap_lib'] == SOAPPY:
      new_creatives = []
      for creative in creatives:
        new_creatives.append(self._message_handler.PackDictAsXml(
            self._sanity_check.ValidateCreative(creative), 'creatives',
            OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_creatives)))
    elif self._config['soap_lib'] == ZSI:
      SanityCheck.ValidateTypes(((creatives, list),))
      new_creatives = []
      for item in creatives:
        new_creatives.append(self._sanity_check.ValidateCreative(
            item, self._web_services))
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'creatives': new_creatives},)),
                                       'Creative', self._loc, request)

  def GetCreative(self, creative_id):
    """Return the creative uniquely identified by the given id.

    Args:
      creative_id: str ID of the creative, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((creative_id, (str, unicode)),))

    method_name = 'getCreative'
    if self._config['soap_lib'] == SOAPPY:
      creative_id = self._message_handler.PackDictAsXml(
          creative_id, 'creativeId', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (creative_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'creativeId': creative_id},)),
                                       'Creative', self._loc, request)

  def GetCreativesByStatement(self, filter_statement):
    """Return a page of creatives that satisfy the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of creatives.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getCreativesByStatement'
    if self._config['soap_lib'] == SOAPPY:
      filter_statement = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateStatement(filter_statement),
          'filterStatement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (filter_statement))
    elif self._config['soap_lib'] == ZSI:
      filter_statement = self._sanity_check.ValidateStatement(
          filter_statement, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'filterStatement': filter_statement},)),
          'Creative', self._loc, request)

  def UpdateCreative(self, creative):
    """Update the specified creative.

    Args:
      company: dict Creative to update.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'updateCreative'
    if self._config['soap_lib'] == SOAPPY:
      creative = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateCreative(creative), 'creative',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (creative))
    elif self._config['soap_lib'] == ZSI:
      creative = self._sanity_check.ValidateCreative(creative,
                                                     self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'creative': creative},)),
                                       'Creative', self._loc, request)


  def UpdateCreatives(self, creatives):
    """Update a list of specified creatives.

    Args:
      companies: list Creatives to update.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'updateCreatives'
    if self._config['soap_lib'] == SOAPPY:
      new_creatives = []
      for creative in creatives:
        new_creatives.append(self._message_handler.PackDictAsXml(
            self._sanity_check.ValidateCreative(creative), 'creatives',
            OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_creatives)))
    elif self._config['soap_lib'] == ZSI:
      SanityCheck.ValidateTypes(((creatives, list),))
      new_creatives = []
      for item in creatives:
        new_creatives.append(self._sanity_check.ValidateCreative(
            item, self._web_services))
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'creatives': new_creatives},)),
                                       'Creative', self._loc, request)
