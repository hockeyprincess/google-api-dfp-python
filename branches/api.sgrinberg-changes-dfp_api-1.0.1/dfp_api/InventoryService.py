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

"""Methods to access InventoryService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from dfp_api import SanityCheck as glob_sanity_check
from dfp_api.Errors import ValidationError
from dfp_api.WebService import WebService


class InventoryService(object):

  """Wrapper for InventoryService.

  The Inventory Service provides operations for creating, updating and
  retrieving ad units.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits InventoryService.

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

  def CreateAdUnit(self, ad_unit):
    """Create a new ad unit.

    Args:
      ad_unit: dict an ad unit to create.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateAdUnit(ad_unit)

    method_name = 'createAdUnit'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'adUnit': ad_unit},)),
                                     'Inventory', self.__loc, request)

  def CreateAdUnits(self, ad_units):
    """Create a list of new ad units.

    Args:
      ad_units: list the ad units to create.

    Returns:
      tuple The response from the API method.
    """
    glob_sanity_check.ValidateTypes(((ad_units, list),))
    for item in ad_units:
      self.__sanity_check.ValidateAdUnit(item)

    method_name = 'createAdUnits'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'adUnits': ad_units},)),
                                     'Inventory', self.__loc, request)

  def GetAdUnit(self, ad_unit_id):
    """Return the ad unit uniquely identified by the given id.

    Args:
      ad_unit_id: str ID of the ad unit, which must already exist.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((ad_unit_id, (str, unicode)),))

    method_name = 'getAdUnit'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'adUnitId': ad_unit_id},)),
                                     'Inventory', self.__loc, request)

  def GetAdUnitsByFilter(self, filter):
    """Return the ad units that match the given filter.

    Args:
      filter: str Publisher Query Language filter.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateFilter(filter)

    method_name = 'getAdUnitsByFilter'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'filter': filter},)),
                                     'Inventory', self.__loc, request)

  def PerformAdUnitAction(self, action, filter):
    """Perform action on ad units that match the given filter.

    Args:
      action: str the action to perform.
      filter: str Publisher Query Language filter.

    Returns:
      tuple response from the API method.
    """
    web_services = self.__web_services
    action = self.__sanity_check.ValidateAction(action, web_services)
    self.__sanity_check.ValidateFilter(filter)

    method_name = 'performAdUnitAction'
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'adUnitAction': action},
                                                    {'filter': filter})),
                                     'Inventory', self.__loc, request)

  def UpdateAdUnit(self, ad_unit):
    """Update the specified ad unit.

    Args:
      ad_unit: dict an ad unit to update.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateAdUnit(ad_unit)

    method_name = 'updateAdUnit'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'adUnit': ad_unit},)),
                                     'Inventory', self.__loc, request)

  def UpdateAdUnits(self, ad_units):
    """Update a list of specified ad units.

    Args:
      ad_units: list the ad units to update.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((ad_units, list),))
    for item in ad_units:
      self.__sanity_check.ValidateAdUnit(item)

    method_name = 'updateAdUnits'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'adUnits': ad_units},)),
                                     'Inventory', self.__loc, request)
