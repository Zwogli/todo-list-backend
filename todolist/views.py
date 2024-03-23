from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import TodoItemSerializer
from .models import TodoItem

# Create your views here.


class TodoItemView(APIView):
    authentication_classes = [TokenAuthentication]  # Token must available
    permission_classes = [IsAuthenticated]          # User must loged in

    def get(self, request, format=None):
        todos = TodoItem.objects.filter(author=request.user)
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)


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