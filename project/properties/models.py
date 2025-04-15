from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now  #  Import now()

#  Property Model
class Property(models.Model):
    PROPERTY_TYPES = [
        ('rent', 'Rent'),
        ('buy', 'Buy')
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    bedrooms = models.IntegerField()
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    image = models.ImageField(upload_to='property_images/', default='property_images/default.jpg')
    rating = models.FloatField(default=0.0)
    reviews_count = models.IntegerField(default=0)
    reviews = models.TextField(blank=True)

    def _str_(self):
        return self.name

    def update_rating(self, new_rating):
        total_rating = (self.rating * self.reviews_count) + new_rating
        self.reviews_count += 1
        self.rating = total_rating / self.reviews_count
        self.save()

#  Contact Model
class Contact(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='contact')
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def _str_(self):
        return self.name

# ✅ Booking Model
class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    check_in_date = models.DateField(default=now)
    check_out_date = models.DateField(default=now)
    booking_date = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')

    def _str_(self):
        return f"Booking {self.id} - {self.user.username} for {self.property.name}"

# ✅ Agreement Model
class Agreement(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='agreement')
    agreement_text = models.TextField()
    signed_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Agreement for Booking {self.booking.id}"

# ✅ Payment Model
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment', null=True, blank=True)  # ✅ Add this line
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    card_name = models.CharField(max_length=255)
    card_number = models.BigIntegerField()
  # Store securely in a real app!
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Payment {self.id} - {self.user.username} - ${self.amount}"