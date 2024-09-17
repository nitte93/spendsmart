# serializers.py in your Django app

from rest_framework import serializers
from .models import UploadedFile,Transaction

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'upload_date', 'file_name', 'file', 'user']
        read_only_fields = ['upload_date', 'user', 'file_name']

    # def create(self, validated_data):
    #     # Assuming 'request' is passed to the serializer's context in the view
    #     user = self.context['request'].user
    #     return UploadedFile.objects.create(user=user, **validated_data)
    def save(self, *args, **kwargs):
        print("kwargs in document serializer",kwargs)
        # if 'file_name' in kwargs:
        #     self.file_name = kwargs['file_name']
        super().save(*args, **kwargs)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id','user', 'transaction_date', 'transaction_name', 'withdrawn_amount', 'deposit_amount', 'reference_number', 'closing_balance']

