from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .module import Booking, Property  # type: ignore

@login_required(login_url='login')
def book_now(request, property_id):
    user = request.user
    property_obj = get_object_or_404(Property, id=property_id)
    booking = Booking.objects.create(user=user, property=property_obj)
    return redirect('property_detail', property_id=property_id)