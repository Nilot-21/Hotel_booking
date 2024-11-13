from django.urls import path
from . import views
urlpatterns=[
    path('signup/',views.signup,name="signup"),
    path("sigin/",views.signin,name="signin"),
    path("hotel/",views.hotel_list,name="hotel"),
    path("booking/",views.booking_detail,name="booking"),
    path("hotel/<str:name>/",views.gethotelbyname,name="gethotelbyname"),
    path("booking/<str:hotel_name>/",views.book_hotel,name="bookhotel")
]