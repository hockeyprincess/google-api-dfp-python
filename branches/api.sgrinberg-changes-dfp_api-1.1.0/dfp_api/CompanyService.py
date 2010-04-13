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

"""Methods to access CompanyService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from dfp_api import SanityCheck as glob_sanity_check
from dfp_api.Errors import ValidationError
from dfp_api.WebService import WebService


class CompanyService(object):

  """Wrapper for CompanyService.

  The Company Service provides operations for creating, updating and retrieving
  companies.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CompanyService.

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

  def CreateCompany(self, company):
    """Create a new company.

    Args:
      company: dict a company to create.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateCompany(company)

    method_name = 'createCompany'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'company': company},)),
                                     'Company', self.__loc, request)

  def CreateCompanies(self, companies):
    """Create a list of new companies.

    Args:
      companies: list the companies to create.

    Returns:
      tuple The response from the API method.
    """
    glob_sanity_check.ValidateTypes(((companies, list),))
    for item in companies:
      self.__sanity_check.ValidateCompany(item)

    method_name = 'createCompanies'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'companies': companies},)),
                                     'Company', self.__loc, request)

  def GetCompany(self, company_id):
    """Return the company uniquely identified by the given id.

    Args:
      company_id: str ID of the company, which must already exist.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((company_id, (str, unicode)),))

    method_name = 'getCompany'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'companyId': company_id},)),
                                     'Company', self.__loc, request)

  def GetCompaniesByFilter(self, filter):
    """Return the companies that match the given filter.

    Args:
      filter: str Publisher Query Language filter which specifies the filtering
              criteria over companies.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((filter, dict),))

    method_name = 'getCompaniesByFilter'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'filter': filter},)),
                                     'Company', self.__loc, request)

  def UpdateCompany(self, company):
    """Update the specified company.

    Args:
      company: dict a company to update.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateCompany(company)

    method_name = 'updateCompany'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'company': company},)),
                                     'Company', self.__loc, request)

  def UpdateCompanies(self, companies):
    """Update a list of specified companies.

    Args:
      companies: list the companies to update.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((companies, list),))
    for item in companies:
      self.__sanity_check.ValidateCompany(item)

    method_name = 'updateCompanies'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'companies': companies},)),
                                     'Company', self.__loc, request)
