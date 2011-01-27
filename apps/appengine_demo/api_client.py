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

"""Client script to handle user interface.

Responsible for building web forms, providing get and post handlers, and
maintaining user interface.
"""

import logging
import os
import time

import wsgiref.handlers
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

try:
  import api_worker
except ImportError, e:
  if e.message.find('pyexpat') > -1:
    raise Exception('Incompatible version of pyexpat. Please see step 7 of the '
                    'step-by-step guide in README.')
  raise Exception(e)


# Enable to see a stack trace in a browser, when a handler raises an exception.
DEBUG = False

LOGIN = 'INSERT_GOOGLE_ACCOUNT_LOGIN_EMAIL_HERE'
PASSW = 'INSERT_GOOGLE_ACCOUNT_PASSWORD_HERE'

# Filter statements.
GET_ORDER_FILTER_STATEMENT = {
    'query': 'WHERE id = :id',
    'params': [
        {
            'type': 'LongParam',
            'key': 'id',
            'value': '0'
        }
    ]
}
GET_LINE_ITEMS_FILTER_STATEMENT = {
    'query': 'WHERE orderId = :orderId limit 3',
    'params': [
        {
            'type': 'LongParam',
            'key': 'orderId',
            'value': '0'
        }
    ]
}


class MainPage(webapp.RequestHandler):

  """Implements MainPage."""

  def get(self):
    """Handle get request."""
    output = []
    try:
      try:
        # Load client instance.
        client = api_worker.SetUpClient(LOGIN, PASSW)

        # Get existing advertisers.
        advertisers = api_worker.GetEntities(client, 'Company')
        if not advertisers:
          # Add dummy advertisers.
          advertisers = api_worker.CreateAdvertisers(client)

        # Get existing publisher users.
        pub_users = api_worker.GetEntities(client, 'User')
        salespeople = []
        traffickers = []
        for user in pub_users:
          if user['roleName'] in ('Salesperson',):
            salespeople.append(user)
          elif user['roleName'] in ('Trafficker',):
            traffickers.append(user)

        # Get all existing orders.
        orders = api_worker.GetEntities(client, 'Order')
      except Exception, e:
        msg = str(e)
        output.append('<font color="red"><b>Error</b></font>: %s' % msg)
    finally:
      # Use templates to write output to the page.
      order_name = 'Order #' + str(time.time()).split('.')[0]
      template_values = {'order_name': order_name,
                         'advertisers': advertisers,
                         'salespeople': salespeople,
                         'traffickers': traffickers}
      path = os.path.join(os.path.dirname(__file__),
                          'data', 'tmpl_order_frm_add.html')
      output.append(template.render(path, template_values))

      template_values = {'orders': orders}
      path = os.path.join(os.path.dirname(__file__),
                          'data', 'tmpl_order_frm_get.html')
      output.append(template.render(path, template_values))

      template_values = {'output': output,
                         'url': users.create_logout_url("/"),
                         'user': users.get_current_user().nickname()}
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))

  def post(self):
    """Handle post request."""
    self.redirect('/')


class CreateOrder(webapp.RequestHandler):

  """Implements AddOrder."""

  def post(self):
    """Handle post request."""
    name = self.request.get('name')
    advertiser_id = self.request.get('advertiserId')
    salesperson_id = self.request.get('salespersonId')
    trafficker_id = self.request.get('traffickerId')

    output = []
    try:
      try:
        # Load client instance.
        client = api_worker.SetUpClient(LOGIN, PASSW)

        # Validate empty input.
        if (not name or not advertiser_id or not salesperson_id or
            not trafficker_id):
          self.redirect('/')

        # Create order.
        order = api_worker.CreateOrder(client, name, advertiser_id,
                                       salesperson_id, trafficker_id)
        self.redirect('/manageLineItems?orderId=%s' % order['id'])
      except Exception, e:
        output.append('<font color="red"><b>Error</b></font>: %s' % e)
    finally:
      # Use template to write output to the page.
      template_values = {'output': output,
                         'url': users.create_logout_url("/"),
                         'user': users.get_current_user().nickname()}
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))


class LookUpOrder(webapp.RequestHandler):

  """Implements LookUpOrder."""

  def post(self):
    """Handle post request."""
    order_id = self.request.get('orderId')
    self.redirect('/manageLineItems?orderId=%s' % order_id)


class ManageLineItems(webapp.RequestHandler):

  """Implements ManageLineItems."""

  def get(self):
    """Handle get request."""
    order_id = self.request.get('orderId')

    output = []
    try:
      try:
        # Load client instance.
        client = api_worker.SetUpClient(LOGIN, PASSW)

        # Get existing order.
        order_filter_statement = GET_ORDER_FILTER_STATEMENT
        order_filter_statement['params'][0]['value'] = order_id
        order = api_worker.GetEntities(client, 'Order', '',
            order_filter_statement)[0]['results'][0]

        # Get 3 line items for existing order.
        line_items_filter_statement = GET_LINE_ITEMS_FILTER_STATEMENT
        line_items_filter_statement['params'][0]['value'] = order_id
        line_items = api_worker.GetEntities(client, 'LineItem', '',
            line_items_filter_statement)[0]['results']
        line_items_output = []
        if not line_items:
          line_items_output.append('<tr><td><center>No line items.</center>'
                                   '<br/><br/></td></tr>')
        else:
          line_items_output.append('<center>First 3 line items</center>')
          # Display existing line items.
          for line_item in line_items:
            form = api_worker.ReadFile(os.path.join(
                'data', 'tmpl_li_frm_manage.html')) % (
                    'editLineItemFormFor' + line_item['id'],
                    order_id, line_item['id'],
                    line_item['name'],
                    line_item['costPerUnit']['microAmount'],
                    line_item['unitsBought'],
                    'Update line item')
            line_items_output.append(api_worker.ReadFile(os.path.join(
                'data', 'tmpl_li_update.html')) % (
                    line_item['id'], line_item['name'], line_item['status'],
                    line_item['id'], form))

        # Display option to create a line item.
        frm_line_item = api_worker.ReadFile(os.path.join(
            'data', 'tmpl_li_frm_manage.html')) % (
                'createLineItemForm', order_id, '',
                'Line item #' + str(time.time()).split('.')[0],
                '2000000', '500000', 'Create line item') + (
            '<div onClick="document.getElementById(\'createLineItemForm\').'
            'style.display=\'block\'; this.style.display=\'none\';" style='
            '"cursor:pointer; color:grey;">&nbsp;[+] Expand to create a line '
            'item</div>')
        line_items_output.append(api_worker.ReadFile(os.path.join(
            'data', 'tmpl_li_add.html')) % frm_line_item)

        # Display order page.
        output.append(api_worker.ReadFile(os.path.join(
            'data', 'tmpl_order.html')) % (
                order['id'], order['name'], order['advertiserId'],
                order['salespersonId'], order['traffickerId'],
                ''.join(line_items_output), order['advertiserId'], order['id']))
      except Exception, e:
        msg = str(e)
        output.append('&nbsp;<font color="red"><b>Error</b></font>: %s' % msg)
    finally:
      # Use template to write output to the page.
      template_values = {'output': output,
                         'url': users.create_logout_url("/"),
                         'user': users.get_current_user().nickname()}
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))

  def post(self):
    """Handle post request."""
    order_id = self.request.get('orderId')
    line_item = {}
    line_item_id = self.request.get('lineItemId')
    if not line_item_id:
      self.redirect('/manageLineItems?orderId=%s' % order_id)
    line_item['name'] = self.request.get('name')
    line_item['lineItemType'] = self.request.get('lineItemType')
    line_item['microAmount'] = self.request.get('microAmount')
    line_item['unitsBought'] = self.request.get('unitsBought')
    line_item['unitType'] = self.request.get('unitType')

    # Load client instance.
    client = api_worker.SetUpClient(LOGIN, PASSW)

    output = []
    try:
      try:
        if line_item_id:
          # Edit line item.
          line_item['id'] = line_item_id
          api_worker.UpdateLineItem(client, order_id, line_item)
        else:
          # Create line item.
          api_worker.CreateLineItem(client, order_id, line_item)
        self.redirect('/manageLineItems?orderId=%s' % order_id)
      except Exception, e:
        msg = str(e)
        output.append('&nbsp;<font color="red"><b>Error</b></font>: %s' % msg)
    finally:
      # Use template to write output to the page.
      template_values = {'output': output,
                         'url': users.create_logout_url("/"),
                         'user': users.get_current_user().nickname()}
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))


class ManageCreatives(webapp.RequestHandler):

  """Implements ManageCreatives."""

  def get(self):
    """Handle get request."""
    advertiser_id = self.request.get('advertiserId')
    order_id = self.request.get('orderId')

    output = []
    try:
      try:
        # Load client instance.
        client = api_worker.SetUpClient(LOGIN, PASSW)

        # Get 3 line items for existing order.
        line_items_filter_statement = GET_LINE_ITEMS_FILTER_STATEMENT
        line_items_filter_statement['params'][0]['value'] = order_id
        line_items = api_worker.GetEntities(client, 'LineItem', '',
            line_items_filter_statement)[0]['results']
        if not line_items:
          output.append(api_worker.ReadFile(os.path.join(
              'data', 'tmpl_cr_no_li.html')) % (advertiser_id, order_id))
        else:
          # Upload dummy creatives.
          creatives = api_worker.CreateCreatives(client, advertiser_id)

          creatives_output = ''
          for creative in creatives:
            line_item_drop_down = ('<select name="%s"><option>----Choose line '
                                   'item----</option>' % creative['id'])
            for line_item in line_items:
              line_item_drop_down += '<option value="%s">%s</option>' % (
                  line_item['id'], line_item['name'])
            line_item_drop_down += '</select>'

            creatives_output += api_worker.ReadFile(os.path.join(
                'data', 'tmpl_cr_row.html')) % (
                    creative['previewUrl'], creative['name'],
                    creative['size']['width'] + 'x' +
                    creative['size']['height'], line_item_drop_down)

          # Display creatives page.
          output.append(api_worker.ReadFile(os.path.join(
              'data', 'tmpl_cr_frm_manage.html')) % (
                  advertiser_id, order_id,
                  advertiser_id, creatives_output))
      except Exception, e:
        msg = str(e)
        output.append('&nbsp;<font color="red"><b>Error</b></font>: %s' % msg)
    finally:
      # Use template to write output to the page.
      template_values = {'output': output,
                         'url': users.create_logout_url("/"),
                         'user': users.get_current_user().nickname()}
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))

  def post(self):
    """Handle post request."""
    advertiser_id = self.request.get('advertiserId')
    order_id = self.request.get('orderId')
    self.redirect('/manageCreatives?advertiserId=%s&orderId=%s' % (
        advertiser_id, order_id))


class SignOrder(webapp.RequestHandler):

  """Implements ShowSummary."""

  def post(self):
    """Handle post request."""
    advertiser_id = self.request.get('advertiserId')
    order_id = self.request.get('orderId')
    pre_licas = []
    for (key, value) in self.request.params.items():
      if key in ('advertiserId', 'orderId'):
        continue
      if value.isdigit():
        pre_licas.append({'creativeId': key, 'lineItemId': value})

    output = []
    try:
      try:
        # Load client instance.
        client = api_worker.SetUpClient(LOGIN, PASSW)

        # Get existing order.
        order_filter_statement = GET_ORDER_FILTER_STATEMENT
        order_filter_statement['params'][0]['value'] = order_id
        order = api_worker.GetEntities(client, 'Order', '',
            order_filter_statement)[0]['results'][0]

        # Get 3 line items for existing order.
        line_items_filter_statement = GET_LINE_ITEMS_FILTER_STATEMENT
        line_items_filter_statement['params'][0]['value'] = order_id
        line_items = api_worker.GetEntities(client, 'LineItem', '',
            line_items_filter_statement)[0]['results']
        line_items_output = ''
        for line_item in line_items:
          creatives_output = ''
          for pre_lica in pre_licas:
            if pre_lica['lineItemId'] == line_item['id']:
              # Does this lica already exists?
              lica = api_worker.GetEntities(
                  client, 'LineItemCreativeAssociation',
                  'WHERE creativeId = \'%s\' AND lineItemId = \'%s\''
                  % (pre_lica['creativeId'], pre_lica['lineItemId']))
              if not lica:
                api_worker.CreateLica(client, pre_lica['creativeId'],
                                      pre_lica['lineItemId'])

              creative = api_worker.GetEntities(client, 'Creative',
                  'WHERE id = \'%s\'' % pre_lica['creativeId'])[0]
              creatives_output += (
                  '<table width="100%">' +
                  api_worker.ReadFile(os.path.join(
                      'data', 'tmpl_cr_row.html')) % (
                          creative['previewUrl'], creative['name'],
                          creative['size']['width'] + 'x' +
                          creative['size']['height'], '') +
                  '</table>')
          line_items_output += api_worker.ReadFile(os.path.join(
              'data', 'tmpl_li_row.html')) % (
                  line_item['id'], line_item['name'], line_item['status'],
                  creatives_output) + '<br/>'

        # Display sign order page.
        output.append(api_worker.ReadFile(os.path.join(
            'data', 'tmpl_sign_order.html')) % (
                 order['id'], order['name'], advertiser_id,
                 order['salespersonId'], order['traffickerId'],
                 line_items_output))
      except Exception, e:
        msg = str(e)
        output.append('&nbsp;<font color="red"><b>Error</b></font>: %s' % msg)
    finally:
      # Use template to write output to the page.
      template_values = {'output': output,
                         'url': users.create_logout_url("/"),
                         'user': users.get_current_user().nickname()}
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))


def main():
  if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([('/', MainPage),
                                        ('/createOrder', CreateOrder),
                                        ('/lookUpOrder', LookUpOrder),
                                        ('/manageLineItems', ManageLineItems),
                                        ('/manageCreatives', ManageCreatives),
                                        ('/signOrder', SignOrder)],
                                       debug=DEBUG)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
