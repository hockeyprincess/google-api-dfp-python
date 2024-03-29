################################################## 
# OrderService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from OrderService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class OrderServiceLocator:
    OrderServiceInterface_address = "https://www.google.com:443/apis/ads/publisher/v201004/OrderService"
    def getOrderServiceInterfaceAddress(self):
        return OrderServiceLocator.OrderServiceInterface_address
    def getOrderServiceInterface(self, url=None, **kw):
        return OrderServiceSoapBindingSOAP(url or OrderServiceLocator.OrderServiceInterface_address, **kw)

# Methods
class OrderServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: createOrder
    def createOrder(self, request):
        if isinstance(request, createOrderRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createOrderResponse.typecode)
        return response

    # op: createOrders
    def createOrders(self, request):
        if isinstance(request, createOrdersRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createOrdersResponse.typecode)
        return response

    # get: getOrder
    def getOrder(self, request):
        if isinstance(request, getOrderRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getOrderResponse.typecode)
        return response

    # get: getOrdersByStatement
    def getOrdersByStatement(self, request):
        if isinstance(request, getOrdersByStatementRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getOrdersByStatementResponse.typecode)
        return response

    # op: performOrderAction
    def performOrderAction(self, request):
        if isinstance(request, performOrderActionRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(performOrderActionResponse.typecode)
        return response

    # op: updateOrder
    def updateOrder(self, request):
        if isinstance(request, updateOrderRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateOrderResponse.typecode)
        return response

    # op: updateOrders
    def updateOrders(self, request):
        if isinstance(request, updateOrdersRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateOrdersResponse.typecode)
        return response

createOrderRequest = ns0.createOrder_Dec().pyclass

createOrderResponse = ns0.createOrderResponse_Dec().pyclass

createOrdersRequest = ns0.createOrders_Dec().pyclass

createOrdersResponse = ns0.createOrdersResponse_Dec().pyclass

getOrderRequest = ns0.getOrder_Dec().pyclass

getOrderResponse = ns0.getOrderResponse_Dec().pyclass

getOrdersByStatementRequest = ns0.getOrdersByStatement_Dec().pyclass

getOrdersByStatementResponse = ns0.getOrdersByStatementResponse_Dec().pyclass

performOrderActionRequest = ns0.performOrderAction_Dec().pyclass

performOrderActionResponse = ns0.performOrderActionResponse_Dec().pyclass

updateOrderRequest = ns0.updateOrder_Dec().pyclass

updateOrderResponse = ns0.updateOrderResponse_Dec().pyclass

updateOrdersRequest = ns0.updateOrders_Dec().pyclass

updateOrdersResponse = ns0.updateOrdersResponse_Dec().pyclass
