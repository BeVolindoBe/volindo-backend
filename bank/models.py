from uuid import uuid4

from django.db import models


class BankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    company_name = models.CharField(max_length=400)
    company_address = models.CharField(max_length=400)
    account_number = models.CharField(max_length=40)
    account_clabe = models.CharField(max_length=40)
    bank_name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=40)

    class Meta:
        db_table = 'bank_accounts'
        managed = True

    def __str__(self):
        return f'{self.bank_name}'
