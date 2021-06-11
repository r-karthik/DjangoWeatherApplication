from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render


@api_view(['GET'])
def my_view(request):
    return Response(status=status.HTTP_200_OK, data="Hello")

