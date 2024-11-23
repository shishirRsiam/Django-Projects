import random
import string
from django.db import models
from django.contrib.auth.models import User

def generate_transaction_id():
        transaction_id = random.choice(string.ascii_uppercase)
        for i in range(10):
            if i % 2 == 0:
                transaction_id += str(random.randint(0, 9)) 
            else:
                transaction_id += random.choice(string.ascii_uppercase)
        return transaction_id

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    transaction_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=0) # 0: pending, 1: completed
    after_transaction_balance = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=1)
    updated_at = models.DateTimeField(auto_now=True, null=1)

    transaction_id = models.CharField(
        max_length=15,
        default=generate_transaction_id,
        editable=False
    )

    def __str__(self):
        return f"{self.user.first_name}: {self.transaction_id} - {self.transaction_type} - {self.amount}"


class Loan(Transaction): 
    purpose = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    repayment_frequency = models.CharField(max_length=50)
    approve_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_admin', null=1)
    

class B2B(Transaction):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_b2b', null=1)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_b2b', null=1)
    b2b_money = models.BooleanField(default=1, null=1)