from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import UploadedFile, Transaction, UploadedFile
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from .forms import UploadFileForm, DocumentForm
import xlrd
import pandas as pd
from datetime import datetime
from dateutil import parser
from decimal import Decimal, InvalidOperation
import logging
import re
from django.db import connection
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine
from langchain.sql_database import SQLDatabase
import urllib.parse
import logging
from rest_framework import generics
from .serializers import DocumentSerializer,TransactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

encoded_password = urllib.parse.quote('Niharikaa@0823')
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Setup basic configuration for logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Create your views here.
def index(request, question_id):
    return Response(data=[question_id], status=status.HTTP_200_OK)

@api_view(['GET'])
def chat(request, question_id):
    data = [{'message': 'Hello, world!', 'sender': 'admin'},
            {'message': 'Hello Admin', 'sender': 'user'},
            {'message': 'what is going on ?', 'sender': 'admin'}, 
            {'message': 'Nothing, just Chatting to you.', 'sender': 'user'}, 
            {'message': 'what is your name ?', 'sender': 'admin'}]
    return Response(data=data, status=status.HTTP_200_OK)


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
    logging.error("error_msg")
    logger.error("Request method: %s", request.method)
    if request.method == 'POST':
        logger.error("Request method1: %s", "sandas")
        form = DocumentForm(request.POST, request.FILES)
        logger.error("Request method1: %s", form)
        if form.is_valid():
            file = request.FILES['file']
            new_doc = form.save(commit=False)
            # new_doc.user = request.user
            new_doc.file_name = request.FILES['file'].name  # Set the file name from the uploaded file
            new_doc.save()
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
                        document=new_doc,
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
            return JsonResponse({'success': False, 'errors': 'Invalid form'}, status=400)

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
    

def list_customers_raw(request):
    with connection.cursor() as cursor:


        # Setup database
        # db = SQLDatabase.from_uri(
        #     f"postgresql+psycopg2://postgres:{env('dbpass')}@localhost:5433/tasks",
        # )
        # Formulate the connection string
        username = "postgres"
        hostname = "localhost"
        database = "mysiteDB"
        port = "5432"
        connection_string = f"postgresql+psycopg2://{username}:{encoded_password}@{hostname}:{port}/{database}"

        # db = SQLDatabase.from_uri('postgresql+psycopg2://postgres:Niharikaa@0823@localhost:5432/mysiteDB')
        db = SQLDatabase.from_uri(connection_string)
        chain = create_sql_query_chain(llm, db)
        # response = chain.invoke({"question": "Give me all the distinct transactions that was done towards swiggy. Show the list without any Limit."})
        response = chain.invoke({"question": "You are an SQL expert, you are working with postgres database, you are given a database that contains the customers bank spending document. Give me all the distinct transactions that was done towards swiggy. Show the list without any Limit. Also while you're retrieving the documents, keep in mind that the transactions can be described in upper case or lower case. "})

        # cursor.execute("SELECT * FROM uploads_transaction")
        cursor.execute("SELECT DISTINCT t.reference_number FROM uploads_transaction t WHERE t.transaction_name LIKE '%swiggy%'")
        # cursor.execute(response)
        rows = cursor.fetchall()
        output = db.run(response)

    # toutput = [{'name': row[0], 'email': row[1], 'created_at': row[2]} for row in output]

    customers = [{'name': row[0], 'email': row[1], 'created_at': row[2]} for row in rows]
    return JsonResponse({'output': output, 'customers': customers, 'query':response})


class DocumentListView(generics.ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = DocumentSerializer


class DocumentDetailView(APIView):
    def get(self, request, document_id, format=None):
        try:
            document = UploadedFile.objects.get(id=document_id)
            documentserializer = DocumentSerializer(document)

            transaction = Transaction.objects.filter(document_id=document_id)
            transactiondocumentserializer = TransactionSerializer(transaction, many=True)
            # Check if the user is the owner or the document is shared with them
            # if document.user == request.user or request.user in document.shared_with.all():
            #     serializer = DocumentSerializer(document)
            #     return Response(serializer.data)
            # else:
            #     return Response({'message': 'Not authorized to view this document.'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'document':documentserializer.data, 'transactions': transactiondocumentserializer.data})
        except UploadedFile.DoesNotExist:
            return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)


class ChatWithRag(APIView):
    # permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated

    def post(self, request, question_id,format=None):
        # Accessing user's posted data:
        user_data = request.data  # This will contain all data sent in the POST request
        message = user_data.get('message', '')  # Safely get the message key from the posted data
        documendId = user_data.get('documentId', '')  # Safely get the documentId key from the posted data
        
        username = "postgres"
        hostname = "localhost"
        database = "mysiteDB"
        port = "5432"
        connection_string = f"postgresql+psycopg2://{username}:{encoded_password}@{hostname}:{port}/{database}"

        # db = SQLDatabase.from_uri('postgresql+psycopg2://postgres:Niharikaa@0823@localhost:5432/mysiteDB')
        db = SQLDatabase.from_uri(connection_string)
        chain = create_sql_query_chain(llm, db)
        # response = chain.invoke({"question": "Give me all the distinct transactions that was done towards swiggy. Show the list without any Limit."})
        response = chain.invoke({"question": "You are an SQL expert, you are working with postgres database,  you are given a database that contains the customers bank spending document. Give me all the distinct transactions that was done towards swiggy. Show the list without any Limit. Also while you're retrieving the documents, keep in mind that the transactions can be described in upper case or lower case. "})

        # cursor.execute("SELECT * FROM uploads_transaction")
        output = db.run(response)

        # Optional: do something with the message, like save it to the database
        response_data = {
            'output': message,
            'response': 'We have received your message.',
            'message': output,
            'sender': 'admin'
        }

        # Return a response
        return Response(response_data, status=200)
