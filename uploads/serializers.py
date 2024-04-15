# serializers.py in your Django app

from rest_framework import serializers
from .models import UploadedFile,Transaction

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'upload_date', 'file_name', 'file']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'transaction_date', 'transaction_name', 'withdrawn_amount', 'deposit_amount', 'reference_number', 'closing_balance']

