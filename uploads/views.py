from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import UploadedFile, Transaction
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from .forms import UploadFileForm
import xlrd
import pandas as pd
from datetime import datetime
from dateutil import parser
from decimal import Decimal, InvalidOperation
import logging
import re

# Setup basic configuration for logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Create your views here.
def index(request, question_id):
    return HttpResponse("You're inside upload index %s." % question_id)


@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        uploaded_file = UploadedFile(file=file)
        uploaded_file.save()
        return JsonResponse({'message': 'File uploaded successfully!'}, status=200)

    return JsonResponse({'error': 'An error occurred'}, status=400)

@api_view(['POST'])
def upload_and_parse_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            try:
                if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                    data = pd.read_excel(file, engine='openpyxl')  # Handles both .xls and .xlsx
                elif file.name.endswith('.csv'):
                    data = pd.read_csv(file)
                else:
                    raise ValueError("Unsupported file format")
            except Exception as e:
                error_msg = f"Error reading file : {e}"
                logging.error(error_msg)

                return JsonResponse({'success': False, 'errors': 'Error reading file'}, status=400)

            errors = []
            for index, row in data.iterrows():
                try:
                    transaction_date = parser.parse(str(row['transaction_date'])).date()
                    transaction_name = str(row['transaction_name'])
                    reference_number = str(row['transaction_reference_number'])

                    # Handle optional decimal fields safely
                    withdrawn_amount = handle_decimal(row['withdrawn_amount'])
                    deposit_amount = handle_decimal(row['deposit_amount'])
                    closing_balance = handle_decimal(row['closing_balance'])


                    # if pd.notna(withdrawn_amount):
                    #     withdrawn_amount = Decimal(withdrawn_amount)
                    # if pd.notna(deposit_amount):
                    #     deposit_amount = Decimal(deposit_amount)
                    # closing_balance = Decimal(closing_balance)
                    
                    Transaction.objects.create(
                        transaction_date=transaction_date,
                        transaction_name=transaction_name,
                        withdrawn_amount=withdrawn_amount,
                        deposit_amount=deposit_amount,
                        reference_number=reference_number,
                        closing_balance=closing_balance
                    )

                except Exception as e:
                    error_msg = f"Error processing row {index + 1}: {e}"
                    errors.append(error_msg)
                    logging.error(error_msg)
                    
            if errors:
                return JsonResponse({'success': False, 'errors': errors}, status=400)


            return JsonResponse({'success': True, 'message': 'File processed successfully'}, status=200)

    else:
        form = UploadFileForm()
        # If not POST or form not valid, return error
        return JsonResponse({'success': False, 'errors': 'Invalid request or form data'}, status=400)



def handle_decimal(value):
    if pd.isna(value):
        return None  # Handle NaN values immediately by returning None
    
    # Clean the string by removing unwanted characters
    # This regex will remove everything except digits, the minus sign, and the decimal point
    cleaned_value = re.sub(r'[^\d.-]', '', str(value))
    
    try:
        # Convert the cleaned string to Decimal
        return Decimal(cleaned_value)
    except InvalidOperation:
        # Log or handle the failed conversion if needed
        return None  # Return None if conversion fails