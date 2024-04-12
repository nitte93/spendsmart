from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploadsDIR/')

    def __str__(self):
        return self.file.name

from django.db import models

class Transaction(models.Model):
    transaction_date = models.DateField()
    transaction_name = models.CharField(max_length=255)
    withdrawn_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reference_number = models.CharField(max_length=255)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.transaction_name} on {self.transaction_date}"
