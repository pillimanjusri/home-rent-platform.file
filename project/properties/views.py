from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Property, Contact
from django.contrib.auth.decorators import login_required
from .models import Property, Booking ,Payment
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from datetime import datetime  # ✅ Import datetime
from django.shortcuts import render
import json
from .models import Payment 
from io import BytesIO
from django.shortcuts import render
from decimal import Decimal 
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt


# from django.shortcuts import render

# post-property code

def property_list(request):
    rent_properties = Property.objects.filter(property_type='Rent')
    buy_properties = Property.objects.filter(property_type='Buy')
    return render(request, 'properties/index.html', {
        'rent_properties': rent_properties,
        'buy_properties': buy_properties
    })

# def post_property(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         location = request.POST.get('location')
#         price = request.POST.get('price')
#         bedrooms = request.POST.get('bedrooms')
#         property_type = request.POST.get('property_type')
#         image = request.FILES.get('image')

#         contact_name = request.POST.get('contact_name')
#         contact_phone = request.POST.get('contact_phone')
#         contact_email = request.POST.get('contact_email')

        # property_obj = Property.objects.create(
        #     name=name,
        #     location=location,
        #     price=price,
        #     bedrooms=bedrooms,
        #     property_type=property_type,
        #     image=image
        # )

        # property_instance =Property.objects.create(
        #     name=name,
        #     location=location,
        #     price=price,
        #     bedrooms=bedrooms,
        #     property_type=property_type,
        #     image=image  # Make sure this matches your model field
        # )

        # Contact.objects.create(
        #     property=property_instance,
        #     name=contact_name,
        #     phone=contact_phone,
        #     email=contact_email
        # )


    #     return redirect('property_list')

    # return render(request, 'properties/post_property.html')




def post_property(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        budget_lacs = float(request.POST.get('budget_lacs', 0))  # Convert to float
        budget_thousands = float(request.POST.get('budget_thousands', 0))  # Convert to float
        price = (budget_lacs * 100000) + (budget_thousands * 1000)
        bedrooms = request.POST.get('bedrooms')
        property_type = request.POST.get('property_type')
        image = request.FILES.get('image')

        # ✅ Get Ratings & Reviews
        rating = request.POST.get('rating')
        reviews = request.POST.get('reviews')

        # Convert rating to float if provided
        rating = float(rating) if rating else 0.0

        contact_name = request.POST.get('contact_name')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')


        # ✅ Save Property with Ratings & Reviews


        # property_obj = Property.objects.create(
        #     name=name,
        #     location=location,
        #     price=price,
        #     bedrooms=bedrooms,
        #     property_type=property_type,
        #     image=image,
        #     rating=rating,  # Save rating
        #     reviews=reviews,  # Save reviews
        #  )



        property_instance = Property.objects.create(
            name=name,
            location=location,
            price=price,
            bedrooms=bedrooms,
            property_type=property_type,
            image=image,
            rating=rating,  # Save rating
            reviews=reviews,  # Save reviews
            reviews_count=len(reviews) if reviews else 0  # Count reviews dynamically
        )

        Contact.objects.create(
            property=property_instance,
            name=contact_name,
            phone=contact_phone,
            email=contact_email
         )


        return redirect('property_list')

    return render(request, 'properties/post_property.html')



# def property_list(request):
#     properties = Property.objects.all().annotate(
#         reviews_count=Count('reviews'),
#         rating=Avg('reviews__rating')
#     )
#     return render(request, "property_list.html", {"properties": properties})


# sign-in and sign-up code

def index(request):
    return render(request, 'properties/index.html')  # Load the main page

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)  # Auto login after sign-up
        return redirect('index')  # Redirect to main page

    return render(request, 'accounts/signin.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to main page
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'accounts/signin.html')


def logout_view(request):
    logout(request)
    return redirect('index')

# Fetch contact details
# def get_contact_details(request, property_id):
#     property_instance = get_object_or_404(Property, id=property_id)
#     contact = Contact.objects.filter(property=property_instance).first()
    
#     if contact:
#         return JsonResponse({
#             'success': True,
#             'name': contact.name,
#             'phone': contact.phone,
#             'email': contact.email
#         })
#     else:
#         return JsonResponse({'success': False})


def get_contact_details(request, property_id):
    try:
        contact = Contact.objects.get(property_id=property_id)
        return JsonResponse({
            'success': True,
            'name': contact.name,
            'phone': contact.phone,
            'email': contact.email
        })
    except contact.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'contact details not found'})
    



# def book_now(request, property_id):
#     property_obj = get_object_or_404(Property, id=property_id)
    
#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
        
#         try:
#             booking = Booking.objects.create(
#                 property=property_obj,
#                 user=request.user,
#                 start_date=start_date,
#                 end_date=end_date,
#                 status='pending'
#             )
#             messages.success(request, 'Property booked successfully!')
#             return redirect('booking_confirmation')
        
#         except Exception as e:
#             messages.error(request, f'Error booking property: {str(e)}')
#             return redirect('property_detail', property_id=property_id)
    
#     return render(request, 'properties/book_now.html', {'property': property_obj})


# @login_required(login_url='/signin/')
# def book_now(request, property_id):
#     property_obj = get_object_or_404(Property, id=property_id)

#     if request.method == 'POST':
#         # Form nunchi booking details techadam
#         check_in_date = request.POST.get('check_in_date')  # Booking start date
#         check_out_date = request.POST.get('check_out_date')  # Booking end date

#         # Booking create cheyyadam
#         booking = Booking.objects.create(
#             user=request.user,  # Logged-in user
#             property=property_obj,  # Property object
#             check_in_date=check_in_date,
#             check_out_date=check_out_date,
        
        
#         )

#         # Booking ayyaka agreement page ki redirect cheyyadam
#         return redirect('agreement', booking_id=booking.id)

#     return render(request, 'properties/book_now.html', {'property': property_obj})




@login_required(login_url='/signin/')
def book_now(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        # Form nunchi booking details techadam
        check_in_date = request.POST.get('check_in_date')  # Booking start date
        check_out_date = request.POST.get('check_out_date')  # Booking end date
        
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format", status=400)

        # Check in date check cheyyadam
        if check_in_date >= check_out_date:
            return HttpResponse("Check-out date must be after check-in date.", status=400)

        # Booking create cheyyadam
        booking = Booking.objects.create(
            user=request.user,  # Logged-in user
            property=property_obj,  # Property object
            check_in_date=check_in_date,
            check_out_date=check_out_date,
           
        )

        # Booking ayyaka agreement page ki redirect cheyyadam
        return redirect('agreement', booking_id=booking.id)

    return render(request, 'properties/book_now.html', {'property': property_obj})



def agreement(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'properties/agreement.html', {'booking': booking})

def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Retrieve payment record, if exists
    payment = Payment.objects.filter(booking=booking).first()

    return render(request, "properties/payment.html", {"booking": booking, "payment": payment})






@login_required
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        card_name = request.POST.get("card_name")
        card_number = request.POST.get("card_number")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")
        amount = request.POST.get("amount")
        

        if not (card_name and card_number and expiry_date and cvv and amount):
            messages.error(request, "Please fill in all the fields.")
            return redirect("payment", booking_id=booking_id)
        try:
            amount_decimal = Decimal(float(amount))  # Convert safely
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount format.")
            return redirect("payment", booking_id=booking_id)


        # Save payment record in the database
        payment = Payment.objects.create(
        booking=booking,
        user=request.user,
        amount=amount_decimal,
        card_name=card_name,
        card_number=card_number,  # Storing insecurely, not ideal!
        expiry_date=expiry_date,
        cvv=cvv,
        
)

        messages.success(request, "Payment successful!")
        return redirect("payment", booking_id=booking_id)  # ✅ Reload payment page with updated data

    return render(request, 'payment.html', {'booking': booking})






def download_invoice(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Format invoice better
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "INVOICE")

    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Payment ID: {payment.id}")
    p.drawString(100, 730, f"User: {payment.user.username}")
    p.drawString(100, 710, f"Amount: ${payment.amount}")
    p.drawString(100, 690, f"Payment Date: {localtime(payment.payment_date).strftime('%Y-%m-%d %H:%M')}")

    # Finalize
    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{payment.id}.pdf"'
    return response





def booking_confirmation(request):
    return render(request, 'properties/booking_confirmation.html')  # Correct template name



def redirect_about(request):
    return redirect("about_us")  # Redirect to correct page

def about_us(request):
    return render(request, "properties/about_us.html")




def index(request):
    properties = Property.objects.all()  # Fetch all properties (both sale & rent)
    return render(request, "properties/index.html", {"properties": properties})




# @login_required
# def add_review(request, property_id):
#     """Allows users to add reviews and ratings to a property"""
#     property_obj = get_object_or_404(Property, id=property_id)

#     if request.method == "POST":
#         rating = int(request.POST.get("rating", 0))
#         comment = request.POST.get("comment", "")

#         if 1 <= rating <= 5:  # ✅ Valid rating check
#             property_obj.update_rating(rating)  # Update rating using model function
#             property_obj.reviews += f"\n{comment}"  # Append review
#             property_obj.save()

#             return redirect("property_detail", property_id=property_id)  # Redirect after review submit

#     return render(request, "properties/add_review.html", {"property": property_obj})


def investment_advice(request):
    return render(request, 'properties/investment_advice.html')













