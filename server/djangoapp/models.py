from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
 
    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# <HINT> Create a plain Python class `DealerReview` to hold review data
    
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.CharField(max_length=50)  # Assuming dealer_id is a string
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
        # Add other choices as needed
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES)
    year = models.DateField()
    # Add any other fields you need for the CarModel model

    def __str__(self):
        return self.name

class CarDealer:
    def __init__(self, dealer_id, name, address):
        self.dealer_id = dealer_id
        self.name = name
        self.address = address

class DealerReview:
    def __init__(self, dealer_id, review):
        self.dealer_id = dealer_id
        self.review = review