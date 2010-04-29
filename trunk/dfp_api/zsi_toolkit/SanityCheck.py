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

"""Validation and type conversion functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from dfp_api import Utils
from dfp_api import SanityCheck as glob_sanity_check
from dfp_api.Errors import ValidationError


def GetPyClass(name, web_services):
  """Return Python class for a given class name.

  Args:
    name: str name of the Python class to return.
    web_services: module for web service.

  Returns:
    Python class.
  """
  return eval('web_services.ns0.%s_Def(\'%s\').pyclass' % (name, name))


def IsPyClass(obj):
  """Return True if a given object is a Python class, False otherwise.

  Args:
    obj: object an object to check.

  Returns:
    bool True if a given object is a Python class, False otherwise.
  """
  if (hasattr(obj, 'typecode') and
      str(obj.typecode.pyclass).find('_Holder') > -1):
    return True
  return False


def ValidateCompany(company):
  """Validate Company object.

  Args:
    company: dict company object.
  """
  glob_sanity_check.ValidateTypes(((company, dict),))
  for key in company:
    glob_sanity_check.ValidateTypes(((company[key], (str, unicode)),))


def ValidateString_ParamMapEntry(param, web_services):
  """Validate String_ParamMapEntry object.

  Args:
    param: dict param object.
    web_services: module for web services.

  Returns:
   String_ParamMapEntry instance.
  """
  if IsPyClass(param):
    return param

  glob_sanity_check.ValidateTypes(((param, dict),))
  new_param = GetPyClass('String_ParamMapEntry', web_services)
  for key in param:
    glob_sanity_check.ValidateTypes(((param[key], (str, unicode)),))
    if key in ('value',):
      if 'type' in param:
        value = GetPyClass(param['type'], web_services)
      else:
        msg = ('The \'type\' of the param is missing.')
        raise ValidationError(msg)
      value.__dict__.__setitem__('_value', param[key])
      new_param.__dict__.__setitem__('_%s' % key, value)
    else:
      new_param.__dict__.__setitem__('_%s' % key, param[key])
  return new_param


def ValidateStatement(statement, web_services):
  """Validate Statement object.

  Args:
    statement: dict statement object.
    web_services: module for web services.

  Returns:
    Statement instance.
  """
  if IsPyClass(statement):
    return statement

  glob_sanity_check.ValidateTypes(((statement, dict),))
  new_statement = GetPyClass('Statement', web_services)
  for key in statement:
    if key in ('params',):
      glob_sanity_check.ValidateTypes(((statement[key], list),))
      params = []
      for param in statement[key]:
        params.append(ValidateString_ParamMapEntry(param, web_services))
      data = params
    else:
      glob_sanity_check.ValidateTypes(((statement[key], (str, unicode)),))
      data = statement[key]
    new_statement.__dict__.__setitem__('_%s' % key, data)
  return new_statement


def ValidateSize(size):
  """Validate Size object.

  Args:
    size: dict size object.
  """
  glob_sanity_check.ValidateTypes(((size, dict),))
  for key in size:
    glob_sanity_check.ValidateTypes(((size[key], (str, unicode)),))


def ValidateCreative(creative, web_services):
  """Validate Creative object.

  A Creative object is one of FlashRedirectCreative, ImageRedirectCreative,
  ThirdPartyCreative, FlashCreative, ImageCreative.

  Args:
    creative: dict creative object.
    web_services: module for web services.

  Returns:
    Creative instance.
  """
  if IsPyClass(creative):
    return creative

  glob_sanity_check.ValidateTypes(((creative, dict),))
  if 'creativeType' in creative:
    new_creative = GetPyClass(creative['creativeType'], web_services)
  elif 'Creative_Type' in creative:
    new_creative = GetPyClass(creative['Creative_Type'], web_services)
  elif 'type' in creative:
    new_creative = GetPyClass(creative['type'], web_services)
  else:
    msg = ('The \'creativeType\' or \'Creative_Type\' or \'type\' of the '
           'creative is missing.')
    raise ValidationError(msg)
  for key in creative:
    if creative[key] == 'None': continue
    if key in ('size', 'flashAssetSize', 'fallbackAssetSize', 'assetSize'):
      ValidateSize(creative[key])
      new_size = GetPyClass('Size', web_services)
      for sub_key in creative[key]:
        new_size.__dict__.__setitem__('_%s' % sub_key, creative[key][sub_key])
      data = new_size
    else:
      glob_sanity_check.ValidateTypes(((creative[key], (str, unicode)),))
      data = creative[key]
    new_creative.__dict__.__setitem__('_%s' % key, data)

  return new_creative


def ValidateSize_StringMapEntry(map_entry):
  """Validate Size_StringMapEntry object.

  Args:
    map_entry: dict size string map entry object.
  """
  glob_sanity_check.ValidateTypes(((map_entry, dict),))
  for key in map_entry:
    if map_entry[key] == 'None': continue
    if key in ('key',):
      ValidateSize(map_entry[key])
    else:
      glob_sanity_check.ValidateTypes(((map_entry[key], (str, unicode)),))


def ValidateAdSenseSettings(settings):
  """Validate AdSenseSettings object.

  Args:
    settings: dict ad sense settings object.
  """
  glob_sanity_check.ValidateTypes(((settings, dict),))
  for key in settings:
    if settings[key] == 'None': continue
    if key in ('afcFormats',):
      glob_sanity_check.ValidateTypes(((settings[key], list),))
      for item in settings[key]:
        ValidateSize_StringMapEntry(item)
    else:
      glob_sanity_check.ValidateTypes(((settings[key], (str, unicode)),))


def ValidateInheritedPropertySource(property_source):
  """Validate InheritedPropertySource object.

  Args:
    property_source: dict inherited property source object.
  """
  glob_sanity_check.ValidateTypes(((property_source, dict),))
  for key in property_source:
    glob_sanity_check.ValidateTypes(((property_source[key], (str, unicode)),))


def ValidateAdSenseSettingsInheritedProperty(property):
  """Validate AdSenseSettingsInheritedProperty object.

  Args:
    property: dict ad sense settings inherited property object.
  """
  glob_sanity_check.ValidateTypes(((property, dict),))
  for key in property:
    if property[key] == 'None': continue
    if key in ('value',):
      ValidateAdSenseSettings(property[key])
    elif key in ('valueSource',):
      ValidateInheritedPropertySource(property[key])


def ValidateAdUnit(ad_unit):
  """Validate AdUnit object.

  Args:
    ad_unit: dict ad unit object.
  """
  glob_sanity_check.ValidateTypes(((ad_unit, dict),))
  for key in ad_unit:
    if ad_unit[key] == 'None': continue
    if key in ('inheritedAdSenseSettings',):
      ValidateAdSenseSettingsInheritedProperty(ad_unit[key])
    elif key in ('sizes',):
      glob_sanity_check.ValidateTypes(((ad_unit[key], list),))
      for item in ad_unit[key]:
        ValidateSize(item)
    else:
      glob_sanity_check.ValidateTypes(((ad_unit[key], (str, unicode)),))


def ValidateDate(date):
  """Validate Date object.

  Args:
    date: dict date object.
  """
  glob_sanity_check.ValidateTypes(((date, dict),))
  for key in date:
    glob_sanity_check.ValidateTypes(((date[key], (str, unicode)),))


def ValidateDateTime(date_time):
  """Validate DateTime object.

  Args:
    date_time: dict date time object.
  """
  glob_sanity_check.ValidateTypes(((date_time, dict),))
  for key in date_time:
    if date_time[key] == 'None': continue
    if key in ('date',):
      ValidateDate(date_time[key])
    else:
      glob_sanity_check.ValidateTypes(((date_time[key], (str, unicode)),))


def ValidateMoney(money):
  """Validate Money object.

  Args:
    money: dict money object.
  """
  glob_sanity_check.ValidateTypes(((money, dict),))
  for key in money:
    glob_sanity_check.ValidateTypes(((money[key], (str, unicode)),))


def ValidateOrder(order):
  """Validate Order object.

  Args:
    order: dict order object.
  """
  glob_sanity_check.ValidateTypes(((order, dict),))
  for key in order:
    if order[key] == 'None': continue
    if key in ('startDateTime', 'endDateTime'):
      ValidateDateTime(order[key])
    elif key in ('totalBudget',):
      ValidateMoney(order[key])
    else:
      glob_sanity_check.ValidateTypes(((order[key], (str, unicode)),))


def ValidateUser(user):
  """Validate User object.

  Args:
    user: dict user object.
  """
  glob_sanity_check.ValidateTypes(((user, dict),))
  for key in user:
    glob_sanity_check.ValidateTypes(((user[key], (str, unicode)),))


def ValidateFrequencyCap(cap):
  """Validate FrequencyCap object.

  Args:
    cap: dict frequency cap object.
  """
  glob_sanity_check.ValidateTypes(((cap, dict),))
  for key in cap:
    glob_sanity_check.ValidateTypes(((cap[key], (str, unicode)),))


def ValidateTargeting(targeting):
  """Validate Targeting object.

  Args:
    targeting: dict targeting object.
    web_services: module for web services.

  Returns:
    Targeting instance.
  """
  if IsPyClass(targeting):
    return targeting

  glob_sanity_check.ValidateTypes(((targeting, dict),))
  for key in targeting:
    if targeting[key] == 'None': continue
    if key in ('inventoryTargeting',):
      glob_sanity_check.ValidateTypes(((targeting[key], dict),))
      target = targeting[key]
      for sub_key in target:
        glob_sanity_check.ValidateTypes(((target[sub_key], list),))
        for item in target[sub_key]:
          glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
        # If value is an empty list, remove key from the dictionary.
        if not target[sub_key]:
          target = Utils.UnLoadDictKeys(target, [sub_key])
      data = target

  return data


def ValidateLineItem(line_item):
  """Validate LineItem object.

  Args:
    line_item: dict line item object.
  """
  glob_sanity_check.ValidateTypes(((line_item, dict),))
  for key in line_item:
    if line_item[key] == 'None': continue
    if key in ('creativeSizes',):
      glob_sanity_check.ValidateTypes(((line_item[key], list),))
      for item in line_item[key]:
        ValidateSize(item)
    elif key in ('startDateTime', 'endDateTime'):
      ValidateDateTime(line_item[key])
    elif key in ('costPerUnit', 'valueCostPerUnit', 'budget'):
      ValidateMoney(line_item[key])
    elif key in ('frequencyCaps',):
      glob_sanity_check.ValidateTypes(((line_item[key], list),))
      for item in line_item[key]:
        ValidateFrequencyCap(item)
    elif key in ('targeting',):
      ValidateTargeting(line_item[key])
    else:
      glob_sanity_check.ValidateTypes(((line_item[key], (str, unicode)),))


def ValidateLica(lica):
  """Validate LICA object.

  Args:
    lica: dict line item creative association object.
  """
  glob_sanity_check.ValidateTypes(((lica, dict),))
  for key in lica:
    if lica[key] == 'None': continue
    if key in ('startTime', 'endTime'):
      ValidateDateTime(lica[key])
    elif key in ('sizes',):
      glob_sanity_check.ValidateTypes(((lica[key], list),))
      for item in lica[key]:
        ValidateSize(item)
    else:
      glob_sanity_check.ValidateTypes(((lica[key], (str, unicode)),))


def ValidatePlacement(placement):
  """Validate Placement object.

  Args:
    placement: dict placement object.
  """
  glob_sanity_check.ValidateTypes(((placement, dict),))
  for key in placement:
    if placement[key] == 'None': continue
    if key in ('targetedAdUnitIds',):
      glob_sanity_check.ValidateTypes(((placement[key], list),))
      for item in placement[key]:
        glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
    else:
      glob_sanity_check.ValidateTypes(((placement[key], (str, unicode)),))


def ValidateAction(action, web_services):
  """Validate Action object.

  An Action is one of AdUnitAction, LineItemCreativeAssociationAction,
  LineItemAction, OrderAction, PlacementAction, UserAction.

  Args:
    action: dict an action to perform.
    web_services: module for web services.

  Returns:
    Action instance.
  """
  if IsPyClass(action):
    return action

  glob_sanity_check.ValidateTypes(((action, dict),))
  if 'type' in action:
    new_action = GetPyClass(action['type'], web_services)
  else:
    msg = 'The \'type\' of the action is missing.'
    raise ValidationError(msg)
  for key in action:
    glob_sanity_check.ValidateTypes(((action[key], (str, unicode)),))
    new_action.__dict__.__setitem__('_%s' % key, action[key])

  return new_action
