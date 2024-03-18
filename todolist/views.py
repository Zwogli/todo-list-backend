from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.

class LoginView(ObtainAuthToken):
  def post(self, request, *args, **kwargs):                                     # Add a POST request
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})        # Work with a serialiser and use the data from outside, data=request.data
        serializer.is_valid(raise_exception=True)                               # If request not valid raise Error
        user = serializer.validated_data['user']                                # Get the user from the POST request
        token, created = Token.objects.get_or_create(user=user)                 # Get or Create Token if user loged in
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })