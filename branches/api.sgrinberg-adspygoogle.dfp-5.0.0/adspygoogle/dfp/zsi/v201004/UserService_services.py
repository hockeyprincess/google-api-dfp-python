################################################## 
# UserService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from UserService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class UserServiceLocator:
    UserServiceInterface_address = "https://www.google.com:443/apis/ads/publisher/v201004/UserService"
    def getUserServiceInterfaceAddress(self):
        return UserServiceLocator.UserServiceInterface_address
    def getUserServiceInterface(self, url=None, **kw):
        return UserServiceSoapBindingSOAP(url or UserServiceLocator.UserServiceInterface_address, **kw)

# Methods
class UserServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: createUser
    def createUser(self, request):
        if isinstance(request, createUserRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createUserResponse.typecode)
        return response

    # op: createUsers
    def createUsers(self, request):
        if isinstance(request, createUsersRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createUsersResponse.typecode)
        return response

    # get: getUserAllRoles
    def getAllRoles(self, request):
        if isinstance(request, getAllRolesRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAllRolesResponse.typecode)
        return response

    # get: getUser
    def getUser(self, request):
        if isinstance(request, getUserRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getUserResponse.typecode)
        return response

    # get: getUsersByStatement
    def getUsersByStatement(self, request):
        if isinstance(request, getUsersByStatementRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getUsersByStatementResponse.typecode)
        return response

    # op: performUserAction
    def performUserAction(self, request):
        if isinstance(request, performUserActionRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(performUserActionResponse.typecode)
        return response

    # op: updateUser
    def updateUser(self, request):
        if isinstance(request, updateUserRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateUserResponse.typecode)
        return response

    # op: updateUsers
    def updateUsers(self, request):
        if isinstance(request, updateUsersRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateUsersResponse.typecode)
        return response

createUserRequest = ns0.createUser_Dec().pyclass

createUserResponse = ns0.createUserResponse_Dec().pyclass

createUsersRequest = ns0.createUsers_Dec().pyclass

createUsersResponse = ns0.createUsersResponse_Dec().pyclass

getAllRolesRequest = ns0.getAllRoles_Dec().pyclass

getAllRolesResponse = ns0.getAllRolesResponse_Dec().pyclass

getUserRequest = ns0.getUser_Dec().pyclass

getUserResponse = ns0.getUserResponse_Dec().pyclass

getUsersByStatementRequest = ns0.getUsersByStatement_Dec().pyclass

getUsersByStatementResponse = ns0.getUsersByStatementResponse_Dec().pyclass

performUserActionRequest = ns0.performUserAction_Dec().pyclass

performUserActionResponse = ns0.performUserActionResponse_Dec().pyclass

updateUserRequest = ns0.updateUser_Dec().pyclass

updateUserResponse = ns0.updateUserResponse_Dec().pyclass

updateUsersRequest = ns0.updateUsers_Dec().pyclass

updateUsersResponse = ns0.updateUsersResponse_Dec().pyclass
