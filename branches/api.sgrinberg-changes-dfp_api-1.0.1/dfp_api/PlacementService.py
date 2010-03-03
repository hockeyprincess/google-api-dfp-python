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

from dfp_api import SanityCheck as glob_sanity_check
from dfp_api.Errors import ValidationError
from dfp_api.WebService import WebService


class PlacementService(object):

  """Wrapper for PlacementService.

  The Placement Service provides methods for creating, updating and retrieving
  placements.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits PlacementService.

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
    self.__web_services = web_services
    self.__loc = eval('web_services.%sLocator()' % self.__class__.__name__)
    self.__sanity_check = SanityCheck

  def CreatePlacement(self, placement):
    """Create a new placement.

    Args:
      placement: dict a placement to create.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidatePlacement(placement)

    method_name = 'createPlacement'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'placement': placement},)),
                                     'Placement', self.__loc, request)

  def CreatePlacements(self, placements):
    """Create a list of new placements.

    Args:
      placements: list the placements to create.

    Returns:
      tuple The response from the API method.
    """
    glob_sanity_check.ValidateTypes(((placements, list),))
    for item in placements:
      self.__sanity_check.ValidatePlacement(item)

    method_name = 'createPlacements'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'placements': placements},)),
                                     'Placement', self.__loc, request)

  def GetPlacement(self, placement_id):
    """Return the placement uniquely identified by the given id.

    Args:
      placement_id: str ID of the placement, which must already exist.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((placement_id, (str, unicode)),))

    method_name = 'getPlacement'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'placementId': placement_id},)),
                                     'Placement', self.__loc, request)

  def GetPlacementsByFilter(self, filter):
    """Return the placements that match the given filter.

    Args:
      filter: str Publisher Query Language filter.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((filter, dict),))

    method_name = 'getPlacementsByFilter'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'filter': filter},)),
                                     'Placement', self.__loc, request)

  def PerformPlacementAction(self, action, filter):
    """Perform action on placements that match the given filter.

    Args:
      action: str the action to perform.
      filter: str Publisher Query Language filter.

    Returns:
      tuple response from the API method.
    """
    web_services = self.__web_services
    action = self.__sanity_check.ValidateAction(action, web_services)
    self.__sanity_check.ValidateFilter(filter)

    method_name = 'performPlacementAction'
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'placementAction': action},
                                                    {'filter': filter})),
                                     'Placement', self.__loc, request)

  def UpdatePlacement(self, placement):
    """Update the specified placement.

    Args:
      placement: dict an placement to update.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidatePlacement(placement)

    method_name = 'updatePlacement'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'placement': placement},)),
                                     'Placement', self.__loc, request)

  def UpdatePlacements(self, placements):
    """Update a list of specified placements.

    Args:
      placements: list the placements to update.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((placements, list),))
    for item in placements:
      self.__sanity_check.ValidatePlacement(item)

    method_name = 'updatePlacements'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'placements': placements},)),
                                     'Placement', self.__loc, request)
