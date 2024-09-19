'''
Question 2: Do django signals run in the same thread as the caller? Please support your answer with a code snippet that 
conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.


'''

''' The direct answer is yes, Django signals run in the same thread as the caller. this means when a signal is Triggered, 
    it executes the same thread as the function that triggered it'''

#Proof that Django signals run in the same thread:

# models.py
from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

# signals.py
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel

@receiver(post_save, sender=TestModel)
def test_signal(sender, instance, **kwargs):
    print(f"Signal is running in thread: {threading.current_thread().name} (ID: {threading.get_ident()})")

# views.py
from django.shortcuts import render
from .models import TestModel
import threading

def test_view(request):
    print(f"View is running in thread: {threading.current_thread().name} (ID: {threading.get_ident()})")
    obj = TestModel.objects.create(name="Test Object")
    return render(request, 'test.html')


'''
The test_view views create a Test_model instace, which triggers the post_save signal.
in both view and the signal handler, we print the current thread's name and id using threading.current_thread().name and threading.get_ident().
If both the view and the signal handler are executed in the same thread, the thread name and ID will be the same in both cases.


As the thread name and ID are the same in both the view and the signal handler, this proves that Django signals run in the same thread as the caller by default.

'''