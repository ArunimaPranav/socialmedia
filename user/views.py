from rest_framework import viewsets, status
from .models import Account
from .serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from datetime import date
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from rest_framework.decorators import action
from chat.models import Messages
from chat.serializers import MessageSerialzer
from django.db.models import Q

# Create your views here.
class UserViewSet(viewsets.ViewSet) :
    permission_classes = [IsAuthenticated]
    
    # Standard actions that will be handled by a router class.
    def list(self, request) :
        queryset = Account.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk) :
        users = Account.objects.all()
        user = get_object_or_404(users, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def destroy(self, request, pk) :
        try :
            queryset = Account.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk) :
        try :
            queryset = Account.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = UserSerializer(instance=user, data=request.data)
            
            if serializer.is_valid() :
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    @action(detail = True,methods=['GET'])
    def chat(self, request, pk):
        chat = Messages.objects.filter(Q(room__sender = request.user) | Q(room__sender = pk) , Q(room__reciever = pk) | Q(room__reciever = request.user))
        serializer = MessageSerialzer(chat , many=True)
        return Response(serializer.data)   
    
class UserRegisterViewSet(viewsets.ViewSet) :
    def create(self, request) :
        serializer = UserSerializer(data=request.data)
        print("hjkasfdjk hasjh fiashif sfhpiuas b")
        print(request.data)
        
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
