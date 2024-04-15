from django.db import models
from django.conf import settings
class UploadedFile(models.Model):

    # document_id: Unique identifier for each document.
    # user_id: Links back to the Users table to identify the owner.
    # upload_date: The date the document was uploaded.
    # file_name: Name of the file.
    # file_path: Path where the file is stored securely.
    upload_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    # file_path = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploadsDIR/')

    def __str__(self):
        return self.file.name

def get_default_document():
    # Attempt to get a default document based on some criteria
    default_document = UploadedFile.objects.filter(file_name="xyz").first()
    if default_document:
        return default_document.id
    else:
        # If no document exists, return None or create a fallback document
        if settings.DEBUG:  # Only automatically create a document in debug mode for safety
            new_document = UploadedFile.objects.create(
                # user=User.objects.filter(is_superuser=True).first(),  # Example: Assign to the first superuser
                file_name='default_document.xls',
                file='/Users/niteshtiwari/Documents/other/spendsmart/media/uploadsDIR/Feb_GroceryBill.pdf'
            )
            return new_document.id
        else:
            # In production, it's safer to return None or handle this explicitly elsewhere
            return None
class Transaction(models.Model):

    # transaction_id: A unique identifier for each transaction.
    # user_id: Identifies which user the transaction belongs to.
    # document_id: Identifies the document from which the transaction was uploaded.
    # transaction_date: Date of the transaction.
    # transaction_type: Type of transaction (e.g., deposit, withdrawal).
    # amount: Transaction amount.
    # reference_number: Transaction reference number.
    # additional_details: Any other pertinent information.

    document = models.ForeignKey(UploadedFile, on_delete=models.CASCADE,default=get_default_document, related_name='transactions')
    transaction_date = models.DateField()
    transaction_name = models.CharField(max_length=255)
    withdrawn_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reference_number = models.CharField(max_length=255)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.transaction_name} on {self.transaction_date}"
