from django.shortcuts import render
from rest_framework import generics
from .serializers import HandbookSerializer
from .models import Handbook
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
# class TerminologyAPIView(generics.ListAPIView): # через сериализер
#    queryset = Handbook.objects.all()
#    serializer_class = HandbookSerializer

class TerminologyAPIView(APIView):
    
    def get(self, request):
        lst = Handbook.objects.all().values()
        return Response({'title': list(lst)})