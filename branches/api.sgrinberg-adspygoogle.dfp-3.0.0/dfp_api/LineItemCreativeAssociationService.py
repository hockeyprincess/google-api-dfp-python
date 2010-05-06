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

"""Methods to access LineItemCreativeAssociationService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from dfp_api import SanityCheck as glob_sanity_check
from dfp_api.Errors import ValidationError
from dfp_api.WebService import WebService


class LineItemCreativeAssociationService(object):

  """Wrapper for LineItemCreativeAssociationService.

  The LineItemCreativeAssociation Service provides operations for creating,
  updating and retrieving line item creative associations (LICA).
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits LineItemCreativeAssociationService.

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

  def CreateLineItemCreativeAssociation(self, lica):
    """Create a new line item creative association.

    Args:
      lica: dict a line item creative association to create.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateLica(lica)

    method_name = 'createLineItemCreativeAssociation'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(
        method_name, (({'lineItemCreativeAssociation': lica},)),
        'LineItemCreativeAssociation', self.__loc, request)

  def CreateLineItemCreativeAssociations(self, licas):
    """Create a list of new line item creative associations.

    Args:
      licas: list the line item creative associations to create.

    Returns:
      tuple The response from the API method.
    """
    glob_sanity_check.ValidateTypes(((licas, list),))
    for item in licas:
      self.__sanity_check.ValidateLica(item)

    method_name = 'createLineItemCreativeAssociations'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(
        method_name, (({'lineItemCreativeAssociations': licas},)),
        'LineItemCreativeAssociation', self.__loc, request)

  def GetLineItemCreativeAssociation(self, line_item_id, creative_id):
    """Return the line item creative association uniquely identified by the
    given line item id and creative id.

    Args:
      line_item_id: str ID of the line item, which must already exist.
      creative_id: str ID of the creative, which must already exist.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((line_item_id, (str, unicode)),
                                     (creative_id, (str, unicode))))

    method_name = 'getLineItemCreativeAssociation'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(
        method_name,
        (({'lineItemId': line_item_id}, {'creativeId': creative_id},)),
        'LineItemCreativeAssociation', self.__loc, request)

  def GetLineItemCreativeAssociationsByStatement(self, filter_statement):
    """Return the line item creative associations that match the given
    statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of line item creative associations

    Returns:
      tuple response from the API method.
    """
    filter_statement = self.__sanity_check.ValidateStatement(filter_statement,
                                                             self._web_services)

    method_name = 'getLineItemCreativeAssociationsByStatement'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(
        method_name, (({'filterStatement': filter_statement},)),
        'LineItemCreativeAssociation', self.__loc, request)

  def PerformLineItemCreativeAssociationAction(self, action, filter_statement):
    """Perform action on line item creative associations that match the given
    statement.

    Args:
      action: dict the action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple response from the API method.
    """
    action = self.__sanity_check.ValidateAction(action, self._web_services)
    filter_statement = self.__sanity_check.ValidateStatement(filter_statement,
                                                             self._web_services)

    method_name = 'performLineItemCreativeAssociationAction'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(
        method_name,
        (({'lineItemCreativeAssociationAction': action},
          {'filterStatement': filter_statement})),
        'LineItemCreativeAssociation', self.__loc, request)

  def UpdateLineItemCreativeAssociation(self, lica):
    """Update the specified line item creative associations.

    Args:
      lica: dict a line item creative association to update.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateLica(lica)

    method_name = 'updateLineItemCreativeAssociation'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(
        method_name, (({'lineItemCreativeAssociation': lica},)),
        'LineItemCreativeAssociation', self.__loc, request)

  def UpdateLineItemCreativeAssociations(self, lica):
    """Update a list of specified line item creative associations.

    Args:
      ad_units: list the line item creative associations to update.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((lica, list),))
    for item in lica:
      self.__sanity_check.ValidateLica(item)

    method_name = 'updateLineItemCreativeAssociations'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(
        method_name, (({'lineItemCreativeAssociations': lica},)),
        'LineItemCreativeAssociation', self.__loc, request)
