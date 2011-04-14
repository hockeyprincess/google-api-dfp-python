################################################## 
# ForecastService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from ForecastService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class ForecastServiceLocator:
    ForecastServiceInterface_address = "https://www.google.com:443/apis/ads/publisher/v201010/ForecastService"
    def getForecastServiceInterfaceAddress(self):
        return ForecastServiceLocator.ForecastServiceInterface_address
    def getForecastServiceInterface(self, url=None, **kw):
        return ForecastServiceSoapBindingSOAP(url or ForecastServiceLocator.ForecastServiceInterface_address, **kw)

# Methods
class ForecastServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getForecast
    def getForecast(self, request):
        if isinstance(request, getForecastRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getForecastResponse.typecode)
        return response

    # get: getForecastById
    def getForecastById(self, request):
        if isinstance(request, getForecastByIdRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getForecastByIdResponse.typecode)
        return response

getForecastRequest = ns0.getForecast_Dec().pyclass

getForecastResponse = ns0.getForecastResponse_Dec().pyclass

getForecastByIdRequest = ns0.getForecastById_Dec().pyclass

getForecastByIdResponse = ns0.getForecastByIdResponse_Dec().pyclass