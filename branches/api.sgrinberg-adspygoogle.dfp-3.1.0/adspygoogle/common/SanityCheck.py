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

"""Validation functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import ETREE
from adspygoogle.common import PYXML
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.Errors import ValidationError


def ValidateRequiredHeaders(headers, required_headers):
  """Sanity check for required authentication elements.

  All required authentication headers have to be set in order to make
  successful API request.

  Args:
    headers: dict Authentication headers.
  """
  is_valid = True
  for headers_set in required_headers:
    is_valid_set = True
    for key in headers_set:
      if key not in headers or not headers[key]: is_valid_set = False
    if not is_valid_set:
      is_valid = False
    else:
      is_valid = True
      break

  if not is_valid:
    msg = ('Required authentication header is missing. Valid options for '
           'headers are %s.' % str(required_headers))
    raise ValidationError(msg)


def IsConfigUserInputValid(user_input, valid_el):
  """Sanity check for user input.

  Args:
    user_input: str User input.
    valid_el: list List of valid elements.

  Returns:
    bool True if user input is valid, False otherwise.
  """
  if not user_input: return False

  try:
    valid_el.index(str(user_input))
  except ValueError:
    return False
  return True


def ValidateConfigSoapLib(soap_lib):
  """Sanity check for SOAP library.

  Args:
    soap_lib: str SOAP library to use.
  """
  if (not isinstance(soap_lib, str) or
      not IsConfigUserInputValid(soap_lib, [SOAPPY, ZSI])):
    msg = ('Invalid input for %s \'%s\', expecting %s or %s of type <str>.'
           % (type(soap_lib), soap_lib, SOAPPY, ZSI))
    raise ValidationError(msg)


def ValidateConfigXmlParser(xml_parser):
  """Sanity check for XML parser.

  Args:
    xml_parser: str XML parser to use.
  """
  if (not isinstance(xml_parser, str) or
      not IsConfigUserInputValid(xml_parser, [PYXML, ETREE])):
    msg = ('Invalid input for %s \'%s\', expecting %s or %s of type <str>.'
           % (type(xml_parser), xml_parser, PYXML, ETREE))
    raise ValidationError(msg)


def IsType(param, param_type):
  """Check if parameter is of the right type.

  Args:
    param: obj Parameter to check.
    param_type: type Type of the parameter to check against.

  Returns:
    bool True if the parameter is of right type, False otherwise.
  """
  if not isinstance(param, param_type):
    return False
  return True


def ValidateTypes(vars_tpl):
  """Check types for a set of variables.

  Args:
    vars_tpl: tuple Set of variables to check.
  """
  for var, var_types in vars_tpl:
    if not isinstance(var_types, tuple):
      var_types = (var_types,)
    for var_type in var_types:
      if IsType(var, var_type):
        return
    msg = ('The \'%s\' is of type %s, expecting one of %s.'
           % (var, type(var), var_types))
    raise ValidationError(msg)


def ValidateOneLevelObject(obj):
  """Validate object with one level of complexity.

  Args:
    obj: dict Object to validate.
  """
  ValidateTypes(((obj, dict),))
  for key in obj:
    if obj[key] != 'None': ValidateTypes(((obj[key], (str, unicode)),))


def ValidateOneLevelList(lst):
  """Validate list with one level of complexity.

  Args:
    lst: list List to validate.
  """
  ValidateTypes(((lst, list),))
  for item in lst:
    if item != 'None': ValidateTypes(((item, (str, unicode)),))
