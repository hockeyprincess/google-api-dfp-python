################################################## 
# NetworkService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from NetworkService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class NetworkServiceLocator:
    NetworkServiceInterface_address = "https://www.google.com:443/apis/ads/publisher/v201010/NetworkService"
    def getNetworkServiceInterfaceAddress(self):
        return NetworkServiceLocator.NetworkServiceInterface_address
    def getNetworkServiceInterface(self, url=None, **kw):
        return NetworkServiceSoapBindingSOAP(url or NetworkServiceLocator.NetworkServiceInterface_address, **kw)

# Methods
class NetworkServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getNetworkAllNetworks
    def getAllNetworks(self, request):
        if isinstance(request, getAllNetworksRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAllNetworksResponse.typecode)
        return response

    # get: getNetworkCurrentNetwork
    def getCurrentNetwork(self, request):
        if isinstance(request, getCurrentNetworkRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getCurrentNetworkResponse.typecode)
        return response

    # op: updateNetwork
    def updateNetwork(self, request):
        if isinstance(request, updateNetworkRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateNetworkResponse.typecode)
        return response

getAllNetworksRequest = ns0.getAllNetworks_Dec().pyclass

getAllNetworksResponse = ns0.getAllNetworksResponse_Dec().pyclass

getCurrentNetworkRequest = ns0.getCurrentNetwork_Dec().pyclass

getCurrentNetworkResponse = ns0.getCurrentNetworkResponse_Dec().pyclass

updateNetworkRequest = ns0.updateNetwork_Dec().pyclass

updateNetworkResponse = ns0.updateNetworkResponse_Dec().pyclass
