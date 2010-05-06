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

"""Methods to access PlacementService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp.DfpWebService import DfpWebService
from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP


class PlacementService(ApiService):

  """Wrapper for PlacementService.

  The Placement Service provides methods for creating, updating and retrieving
  placements.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits PlacementService.

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
    super(PlacementService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreatePlacement(self, placement):
    """Create a new placement.

    Args:
      placement: dict Placement to create.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacement(placement)

    method_name = 'createPlacement'
    if self._config['soap_lib'] == SOAPPY:
      placement = self._message_handler.PackDictAsXml(
          placement, 'placement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (placement))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placement': placement},)),
                                       'Placement', self._loc, request)

  def CreatePlacements(self, placements):
    """Create a list of new placements.

    Args:
      placements: list Placements to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((placements, list),))
    for item in placements:
      self._sanity_check.ValidatePlacement(item)

    method_name = 'createPlacements'
    if self._config['soap_lib'] == SOAPPY:
      new_placements = []
      for placement in placements:
        new_placements.append(self._message_handler.PackDictAsXml(
            placement, 'placements', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_placements)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placements': placements},)),
                                       'Placement', self._loc, request)

  def GetPlacement(self, placement_id):
    """Return the placement uniquely identified by the given id.

    Args:
      placement_id: str ID of the placement, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((placement_id, (str, unicode)),))

    method_name = 'getPlacement'
    if self._config['soap_lib'] == SOAPPY:
      placement_id = self._message_handler.PackDictAsXml(
          placement_id, 'placementId', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (placement_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placementId': placement_id},)),
                                       'Placement', self._loc, request)

  def GetPlacementsByStatement(self, filter_statement):
    """Return the placements that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of placements.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getPlacementsByStatement'
    if self._config['soap_lib'] == SOAPPY:
      filter_statement = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateStatement(filter_statement),
          'filterStatement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (filter_statement))
    elif self._config['soap_lib'] == ZSI:
      filter_statement = self._sanity_check.ValidateStatement(
          filter_statement, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
          (({'filterStatement': filter_statement},)), 'Placement', self._loc,
          request)

  def PerformPlacementAction(self, action, filter_statement):
    """Perform action on placements that match the given statement.

    Args:
      action: str Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'performPlacementAction'
    if self._config['soap_lib'] == SOAPPY:
      self._sanity_check.ValidateAction(action)
      action = self._message_handler.PackDictAsXml(action, 'placementAction',
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
          (({'placementAction': action},
            {'filterStatement': filter_statement})), 'Placement', self._loc,
          request)

  def UpdatePlacement(self, placement):
    """Update the specified placement.

    Args:
      placement: dict Placement to update.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacement(placement)

    method_name = 'updatePlacement'
    if self._config['soap_lib'] == SOAPPY:
      placement = self._message_handler.PackDictAsXml(
          placement, 'placement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (placement))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placement': placement},)),
                                       'Placement', self._loc, request)

  def UpdatePlacements(self, placements):
    """Update a list of specified placements.

    Args:
      placements: list Placements to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((placements, list),))
    for item in placements:
      self._sanity_check.ValidatePlacement(item)

    method_name = 'updatePlacements'
    if self._config['soap_lib'] == SOAPPY:
      new_placements = []
      for placement in placements:
        new_placements.append(self._message_handler.PackDictAsXml(
            placement, 'placements', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_placements)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placements': placements},)),
                                       'Placement', self._loc, request)
