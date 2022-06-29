"""
Views for the User API

"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from user.serializers import (UserSerializer,AuthTokenSerializer)

class CreateUserView(generics.CreateAPIView): # CreateAPIView handles http reuquest to create objects in db automatically
    """Create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES #used to get browsable user interface for the API

class ManageUserView(generics.RetrieveUpdateAPIView): # RetrieveUpdateAPIView used to retrieve  and update objects in db
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication] #type of authentication to use
    permission_classes = [permissions.IsAuthenticated] #user must be authenticated

    def get_object(self): #overriding get  object , by default used to get http requests
        """Retrieve and return the authenticated user."""
        return self.request.user

