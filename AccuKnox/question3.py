'''
Question 3: By default do django signals run in the same database transaction as the caller? Please support your answer with a code 
snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

'''

''' Yes Django signals run in thesame database transaction as the caller. if the signal is triggered with a transactional operation.
    This means that if a database transaction is rolled back, changed made in signal will also roll back. we can prove it by making 
    a scenerio where we can raise an exception in the view after a signal is trigerred, and check whether the changed made in the
    signal handler are rolled back or not.
'''

# models.py
from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class SignalLog(models.Model):
    message = models.CharField(max_length=255)

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel, SignalLog

@receiver(post_save, sender=TestModel)
def test_signal(sender, instance, **kwargs):
    # Signal handler creates a new record in the SignalLog
    SignalLog.objects.create(message=f"Signal triggered for {instance.name}")
    print(f"Signal executed and created log for {instance.name}")

# views.py
from django.shortcuts import render
from .models import TestModel, SignalLog
from django.db import transaction

def test_view(request):
    try:
        with transaction.atomic():
            obj = TestModel.objects.create(name="Test Object")
            print("TestModel instance created")
            # Raise an exception to simulate transaction failure
            raise Exception("Simulated error after object creation")
    except Exception as e:
        print(f"Transaction rolled back: {str(e)}")

    # Check if the log created in the signal handler exists
    logs = SignalLog.objects.all()
    print(f"Logs count: {logs.count()}")
    return render(request, 'test.html')


'''
    1. when we create a Testmodel instance in the test_view the post_save signal is triggered.
    2. The test_signal signal handler creates a log entry in the SignalLog table.
    3. after the signal handler completes, we raise and exception in the view to stimulte a transaction failure.
    4. Because the signal handler runs within the same transaction as the view, when the exception is raised, the entire transaction 
        (including the changes made by the signal handler) will be rolled back.


    this will prove that the django signals run in the same database transaction as the caller by default.    


'''