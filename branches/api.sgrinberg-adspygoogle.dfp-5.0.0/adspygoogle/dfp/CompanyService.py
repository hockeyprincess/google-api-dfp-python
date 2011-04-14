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

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp.DfpWebService import DfpWebService


class CompanyService(ApiService):

  """Wrapper for CompanyService.

  The Company Service provides operations for creating, updating and retrieving
  companies.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CompanyService.

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
    super(CompanyService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateCompany(self, company):
    """Create a new company.

    Args:
      company: dict Company to create.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCompany(company)

    method_name = 'createCompany'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      company = self._message_handler.PackDictAsXml(
          company, 'company', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (company))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'company': company},)),
                                       'Company', self._loc, request)

  def CreateCompanies(self, companies):
    """Create a list of new companies.

    Args:
      companies: list Companies to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((companies, list),))
    for item in companies:
      self._sanity_check.ValidateCompany(item)

    method_name = 'createCompanies'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      new_companies = []
      for company in companies:
        new_companies.append(self._message_handler.PackDictAsXml(
            company, 'companies', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_companies)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'companies': companies},)),
                                       'Company', self._loc, request)

  def GetCompany(self, company_id):
    """Return the company uniquely identified by the given id.

    Args:
      company_id: str ID of the company, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((company_id, (str, unicode)),))

    method_name = 'getCompany'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      company_id = self._message_handler.PackDictAsXml(
          company_id, 'companyId', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (company_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'companyId': company_id},)),
                                       'Company', self._loc, request)

  def GetCompaniesByStatement(self, filter_statement):
    """Return the companies that match the given filter.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of companies.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getCompaniesByStatement'
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
      return self.__service.CallMethod(
          method_name, (({'filterStatement': filter_statement},)),
          'Company', self._loc, request)

  def UpdateCompany(self, company):
    """Update the specified company.

    Args:
      company: dict Company to update.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCompany(company)

    method_name = 'updateCompany'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      company = self._message_handler.PackDictAsXml(
          company, 'company', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (company))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'company': company},)),
                                       'Company', self._loc, request)

  def UpdateCompanies(self, companies):
    """Update a list of specified companies.

    Args:
      companies: list Companies to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((companies, list),))
    for item in companies:
      self._sanity_check.ValidateCompany(item)

    method_name = 'updateCompanies'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      new_companies = []
      for company in companies:
        new_companies.append(self._message_handler.PackDictAsXml(
            company, 'companies', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_companies)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'companies': companies},)),
                                       'Company', self._loc, request)
