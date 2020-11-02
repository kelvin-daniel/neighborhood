from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
import datetime as dt
# Create your tests here.
class neighbourhoodTestClass(TestCase):
    def setUp(self):
        self.donholm = neighbourhood(neighbourhood='donholm')

    def test_instance(self):
        self.assertTrue(isinstance(self.donholm,neighbourhood))

    def tearDown(self):
        neighbourhood.objects.all().delete()

    def test_save_method(self):
        self.donholm.save_neighbourhood()
        hood = neighbourhood.objects.all()
        self.assertTrue(len(hood)>0)

    def test_delete_method(self):
        self.donholm.delete_neighbourhood('donholm')
        hood = neighbourhood.objects.all()
        self.assertTrue(len(hood)==0)
    

class BusinessTestClass(TestCase):
    def setUp(self):
        self.business = Business(name='baazar')

    def test_hood_instance(self):
        self.assertTrue(isinstance(self.business, Business))

    def test_save_business_method(self):
        self.business.save_business()
        business_object = Business.objects.all()
        self.assertTrue(len(business_object) > 0)

    def test_delete_business_method(self):
        self.business.save_business()
        business_object = Business.objects.all()
        self.business.delete_business()
        business_object = Business.objects.all()
        self.assertTrue(len(business_object) == 0)


