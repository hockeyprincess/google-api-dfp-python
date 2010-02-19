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

from dfp_api import ETREE
from dfp_api import PYXML
from dfp_api.Errors import ValidationError


def ValidateRequiredHeaders(headers):
  """Sanity check for required authentication elements.

  All required authentication headers have to be set in order to make
  successful API request.

  Args:
    headers: dict authentication headers.
  """
  req_headers = ('email', 'password', 'applicationName')
  for key in req_headers:
    if key not in headers or not headers[key]:
      msg = ('Required authentication header \'%s\' is missing.' % key)
      raise ValidationError(msg)


def IsConfigUserInputValid(user_input, valid_el):
  """Sanity check for user input.

  Args:
    user_input: str user input.
    valid_el: list of valid elements.

  Returns:
    bool True if user input is valid, False otherwise.
  """
  if not user_input:
    return False

  try:
    valid_el.index(str(user_input))
  except ValueError:
    return False
  return True


def ValidateServer(server, version):
  """Sanity check for API server.

  Args:
    server: str API server to access for this API call.
    version: str API version being used to access the server.
  """
  # Map of supported API servers and versions.
  prod = {'v201002': 'https://www.google.com'}
  sandbox = {'v201002': 'https://sandbox.google.com'}

  if server not in prod.values() and server not in sandbox.values():
    msg = ('Given API server, \'%s\', is not valid. Expecting one of %s.'
           % (server, sorted(prod.values() + sandbox.values())[1:]))
    raise ValidationError(msg)

  if version not in prod.keys() and version not in sandbox.keys():
    msg = ('Geven API version, \'%s\', is not valid. Expecting one of %s.'
           % (version, sorted(set(prod.keys() + sandbox.keys()))))
    raise ValidationError(msg)

  if server != prod[version] and server != sandbox[version]:
    msg = ('Given API version, \'%s\', is not compatible with given server, '
           '\'%s\'.' % (version, server))
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
    param: parameter to check.
    param_type: type of the parameter to check against.

  Returns:
    bool True if the parameter is of right type, False otherwise.
  """
  if not isinstance(param, param_type):
    return False
  return True


def ValidateTypes(vars_tpl):
  """Check types for a set of variables.

  Args:
    vars_tpl: tuple set of variables to check.
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
