from django.test import TestCase
from Dashboard.models import Unit
from random import random

class UnitTest(TestCase):
    def setUp(self):
        Unit.objects.create(title="TestCase1", description="Description", profile_id=0, ratio=.25)

    def test_outlier_filtering(self):
        """Test outlier filtering"""
        test_case_1 = Unit.objects.get(title="TestCase1")
        estimated_value = 20
        for i in range(100):
            test_case_1.update_ratio(estimated_value+random()*5-1)
        test_case_1.update_ratio(10**6) # Adding absurd value. Should be ignored.
        print("Mean at", test_case_1.time_sum/(test_case_1.k-1))
        assert abs(test_case_1.ratio) - 20 < 2 # It should still be around 20