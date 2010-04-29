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

from dfp_api import SanityCheck as glob_sanity_check
from dfp_api.Errors import ValidationError
from dfp_api.WebService import WebService


class CreativeService(object):

  """Wrapper for CreativeService.

  The Creative Service provides methods for adding, updating and retrieving
  creatives.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CreativeService.

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

  def CreateCreative(self, creative):
    """Create a new creative.

    Args:
      creative: dict a creative to create.

    Returns:
      tuple response from the API method.
    """
    web_services = self.__web_services
    creative = self.__sanity_check.ValidateCreative(creative, web_services)

    method_name = 'createCreative'
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'creative': creative},)),
                                     'Creative', self.__loc, request)

  def CreateCreatives(self, creatives):
    """Create a list of new creatives.

    Args:
      creatives: list the creatives to create.

    Returns:
      tuple The response from the API method.
    """
    web_services = self.__web_services
    glob_sanity_check.ValidateTypes(((creatives, list),))
    new_creatives = []
    for item in creatives:
      new_creatives.append(self.__sanity_check.ValidateCreative(
          item, web_services))

    method_name = 'createCreatives'
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'creatives': new_creatives},)),
                                     'Creative', self.__loc, request)

  def GetCreative(self, creative_id):
    """Return the creative uniquely identified by the given id.

    Args:
      creative_id: str ID of the creative, which must already exist.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((creative_id, (str, unicode)),))

    method_name = 'getCreative'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'creativeId': creative_id},)),
                                     'Creative', self.__loc, request)

  def GetCreativesByFilter(self, filter):
    """Return a page of creatives that satisfy the given filter.

    Args:
      filter: str Publisher Query Language filter which specifies the filtering
              criteria over creatives.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateFilter(filter)

    method_name = 'getCreativesByFilter'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'filter': filter},)),
                                     'Creative', self.__loc, request)

  def UpdateCreative(self, creative):
    """Update the specified creative.

    Args:
      company: dict a creative to update.

    Returns:
      tuple response from the API method.
    """
    web_services = self.__web_services
    creative = self.__sanity_check.ValidateCreative(creative, web_services)

    method_name = 'updateCreative'
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'creative': creative},)),
                                     'Creative', self.__loc, request)

  def UpdateCreatives(self, creatives):
    """Update a list of specified creatives.

    Args:
      companies: list the creatives to update.

    Returns:
      tuple response from the API method.
    """
    web_services = self.__web_services
    glob_sanity_check.ValidateTypes(((creatives, list),))
    new_creatives = []
    for item in creatives:
      new_creatives.append(self.__sanity_check.ValidateCreative(
          item, web_services))

    method_name = 'updateCreatives'
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'creatives': new_creatives},)),
                                     'Creative', self.__loc, request)
