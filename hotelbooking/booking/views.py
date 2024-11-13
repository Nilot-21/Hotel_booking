from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Hotel,Booking
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime


#this function is used to perform signup 
@csrf_exempt
@api_view(['POST'])
def signup(request):
    data=json.loads(request.body)
    username=data.get('username')
    password=data.get('password')

    if not username or not password:
        return Response({"error":"'check for username,password"},status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"error":"Username already exists"},status=status.HTTP_400_BAD_REQUEST)
    
    user=User.objects.create_user(username=username,password=password)
    user.save()
    return Response({"message":"User created successfully"},status=status.HTTP_201_CREATED)


#this function view is used to perforrm signin and provide jwt authentication

@csrf_exempt 
@api_view(['POST'])
def signin(request):
    data=json.loads(request.body)
    username=data.get("username")
    password=data.get('password')
    
    user=authenticate(request,username=username,password=password)
    if user is not None:
        token=RefreshToken.for_user(user)
        return Response({
            'refresh':str(token),
            'access':str(token.access_token),
            })
    return Response({"error":"pls enter valid credentials"})

#this function is used to display the lsit of hotel

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hotel_list(request):
    hotels=Hotel.objects.all()
    detail=[{"name":hotel.name,"address":hotel.address} for hotel in hotels]

    return Response(detail)

#this function is used to display booking

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_detail(request):
    user=request.user
    booking=Booking.objects.filter(user=user)
    
    booking_detail=[{
            "Name of the Hotel":book.hotel.name,
            "check_in":book.check_in,
            "check_out":book.check_out
        }for book in booking]
    
    return Response(booking_detail)

#this is used to get hotel by name

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gethotelbyname(request,name):
    try:
        hotel=get_object_or_404(Hotel,name=name)
        hotel_detail={
            "name":hotel.name,
            "address":hotel.address
        }
        return Response(hotel_detail)
    except Exception as e:
        return Response({"error":str(e)})
    
#this is used to book the hotel based on the name of hotel

@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['POST'])
def book_hotel(request,hotel_name):
    try:
        check_in=parse_datetime(request.data.get("check_in"))
        check_out=parse_datetime(request.data.get("check_out"))
        
        if check_in>=check_out:
            return Response({"error":"pls check for checkin checkout date and time"})
        hotel=get_object_or_404(Hotel,name=hotel_name)

        booking=Booking.objects.create(user=request.user,hotel=hotel,check_in=check_in,
                                       check_out=check_out)
        
        return Response({"message":"Booking done successfully"},status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error":str(e)})


