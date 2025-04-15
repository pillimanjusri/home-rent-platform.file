from django.urls import path
from . import views

from django.urls import path
# from .views import user_login, user_signup, user_logout
from .views import property_list, post_property, index, login_view, signup_view, logout_view, get_contact_details,payment, process_payment, about_us, redirect_about, index, download_invoice




urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('post-property/', views.post_property, name='post_property'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('contact/<int:property_id>/', views.get_contact_details, name='get_contact_details'),
    path('book_now/<int:property_id>/', views.book_now, name='book_now'),
    path('agreement/<int:booking_id>/', views.agreement, name='agreement'),

    # Payments & Booking
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('process_payment/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('download_invoice/<int:payment_id>/', views.download_invoice, name='download_invoice'),
    path('booking_confirmation/', views.booking_confirmation, name='booking_confirmation'),  # Fixed naming

    # Other Pages
    path("aboutus.html", redirect_about),  # Redirect old URL
    path("about-us/", about_us, name="about_us"),

    path("", views.index, name="index"),  # Home Page
    path('investment-advice/', views.investment_advice, name='investment_advice'),
]