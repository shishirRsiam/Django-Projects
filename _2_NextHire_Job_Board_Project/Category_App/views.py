from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response

class CategoryViewSet(APIView):
    def get(self, request, format=None):
        data = Category.objects.all()
        serializer = CategorySerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)