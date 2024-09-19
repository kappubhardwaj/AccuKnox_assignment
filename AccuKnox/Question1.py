'''
Question 1: By default are django signals executed synchronously or asynchronously? Please support your answer with a code snippet 
that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic

'''



'''by default Django signals are synchronous. This means whenever a signal in emitted, the receiver function connected to that signal is executed, 
and the code that trigger the sigmal must wait for the receriver function to finish before continuing. however we can make django signal asynchronous
 if needed this can be useful when we are dealing with a time consuming task. like sending mails or making API Calls''' 

#Proof that Django signals are synchronous

# models.py
from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

# signals.py
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel
import datetime

@receiver(post_save, sender=TestModel)
def test_signal(sender, instance, **kwargs):
    print(f"Signal triggered at: {datetime.datetime.now()}")
    time.sleep(5)  
    print(f"Signal completed at: {datetime.datetime.now()}")

# views.py
from django.shortcuts import render
from .models import TestModel
import datetime

def test_view(request):
    print(f"View started at: {datetime.datetime.now()}")
    obj = TestModel.objects.create(name="Test Object")
    print(f"View ended at: {datetime.datetime.now()}")
    return render(request, 'test.html')

''' when we hit the test_view, a new instance of TestModel is created, which triggers the post_save signal.
    the test_signal signal handler has a time.sleep(5) to stimulate a delay of 5 seconds.
    the timestamps will show that the view waits for the signal to complete before running.
    this delay will prove that django signals are executed synchronous by default
'''





