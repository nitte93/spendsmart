import json
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import UploadedFile, Transaction, UploadedFile
# from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.parsers import MultiPartParser,FormParser
from .forms import UploadFileForm, DocumentForm
import xlrd
import pandas as pd
import ast
from datetime import datetime
from dateutil import parser
from decimal import Decimal, InvalidOperation
import logging
import re
from django.db import connection
from langchain.chains import create_sql_query_chain
# from langchain_openai import ChatOpenAI
# from sqlalchemy import create_engine
from langchain.sql_database import SQLDatabase
import urllib.parse
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging
from rest_framework import generics
from .serializers import DocumentSerializer,TransactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from sqlalchemy import create_engine, text
import json
# from langchain.prompts import ChatPromptTemplate
# from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional
import sqlite3
from aiagent.agent import WorkFlowManager
import uuid


logger = logging.getLogger(__name__)

encoded_password = urllib.parse.quote('Niharikaa@0823')
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Setup basic configuration for logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Create your views here.
def index(request, question_id):
    return Response(data=[question_id], status=status.HTTP_200_OK)

@api_view(['GET'])
def chat(request, document_name):
    data = [{'message': 'Hello, world!', 'sender': 'admin'},
            {'message': 'Hello Admin', 'sender': 'user'},
            {'message': 'what is going on ?', 'sender': 'admin'}, 
            {'message': 'Nothing, just Chatting to you.', 'sender': 'user'}, 
            {'message': "what is the maximum amount I've spend on swiggy?", 'sender': 'admin'}]
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
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_and_parse_file(request):
    logging.error("error_msg")
    logger.error("Request method: %s", request.method)
    if request.method == 'POST':
        logger.error("Request method1: %s", "sandas")
        form = DocumentSerializer(data=request.data)

        # logger.error("serialize data: %s", form.initial_data)
        # logger.error("Request method1: %s", form)
        if form.is_valid():
            file = request.FILES['file']
            logger.error("Form content %s", form.validated_data)
            # new_doc = form.save(commit=False)
            file_name = request.FILES['file'].name  # Set the file name from the uploaded file
            user = request.user
            # user=request.user, file_name=request.FILES.get('file').name
            new_doc = form.save(user=request.user, file_name=file_name )
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
                        closing_balance=closing_balance,
                        user=request.user
                    )

                except Exception as e:
                    error_msg = f"Error processing row {index + 1}: {e}"
                    errors.append(error_msg)
                    logging.error(error_msg)
                    
            if errors:
                return JsonResponse({'success': False, 'errors': errors}, status=400)


            return JsonResponse({'success': True, 'message': 'File processed successfully'}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': 'Invalid form', 'serializeerror': form.errors}, status=400)

    else:
        form = UploadFileForm()
        # If not POST or form not valid, return error
        return JsonResponse({'success': False, 'errors': 'Invalid request or form data'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_and_parse_excel_to_sql(request):
    logging.error("Request methods: %s", request.method)

    if request.method == 'POST':
        form = DocumentSerializer(data=request.data)

        if form.is_valid():
            file = request.FILES['file']
            logger.error("Form Content %s", form.validated_data)

            file_name = request.FILES['file'].name
            user = request.user

            # generate unique id for the file
            unique_id = str(uuid.uuid4())

            new_file_name = f"{unique_id}_{file_name}"

            new_doc = form.save(user=user, file_name=new_file_name)


            try:
                if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                    # data = pd.read_excel(file, engine='openpyxl', parse_dates=['transaction_date']) # handle both .xls and .xlsx
                    data = pd.read_excel(file, engine='openpyxl') # handle both .xls and .xlsx
                elif file.name.endswith('.csv'):
                    data = pd.read_csv(file, parse_dates=['transaction_date'])
                else:
                    raise ValueError("Unsupported file format")
            except Exception as e:
                error_msg = f"Error reading file: `{e}`"
                logging.error(error_msg)

                return JsonResponse({'success': False, 'errors': error_msg}, status=400)

            # prepare to write dataframe into SQLite
            try:
                # sqlite path
                # sqlite_file_path = f"./uploadsDir/{new_file_name.split('.')[0]}.db"
                base_name = new_file_name.split('.')[0]
                sqlite_file_path = f"./uploadsDir/{base_name}.db"
                # os.makedirs(os.path.dirname(sqlite_file_path), exist_ok=True)  # Create directory if it doesn't exist


                # create Sqlite connection
                conn = sqlite3.connect(sqlite_file_path)
                logger.error("Connected to sqlite database: %s", sqlite_file_path)

                # write dataframe to sqlite table
                # Set the first row as the header and keep it in the DataFrame
                # data.columns = data.iloc[0]  # Set the first row as the header
                # data = data[1:]  # Remove the header row from the data for processing
                
                try:
                # Parse the date only for the remaining rows
                    data['transaction_date'] = pd.to_datetime(data['transaction_date'], format="%d/%m/%y").dt.strftime('%Y-%m-%d')
                except Exception as e:
                    error_msg = f"Error parsing date in file: {e}"
                    logging.error(error_msg)
                    return JsonResponse({'success': False, 'errors': error_msg}, status=400)
                
                table_name = "transactions"
                data.to_sql(table_name, conn, if_exists='replace', index=True)

                # close connection
                conn.close()

                return JsonResponse({
                    'success': True,
                    'message': 'File processed and stored in SQlite successfully',
                    'db_path': sqlite_file_path,
                }, status=200)
            

            except Exception as e:
                error_msg = f"Error processing file to Sqlite `{e}`"
                logging.error(error_msg)
                return JsonResponse({
                    'success': False,
                    'errors': error_msg
                }, status=500)

        else:
            return JsonResponse({
                'success': False,
                'error': "Invalid form",
                'serialzeerror': form.errors
            },
            status=400
            )
    
    else:
        form = UploadFileForm()

        return JsonResponse({
            'success': False,
            'errors': 'Invalid request method or form data'
        },
        status=400
        )


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

def read_db_content(request, document_name, format=None):
    # Connect to the SQLite database
    logger.error(document_name)
    db_file = f"./uploadsDir/{document_name}.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Execute a query to fetch all data from a specific table
    table_name = 'transactions'  # Replace with your actual table name
    cursor.execute(f"SELECT * FROM `{table_name}`")

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Print the content
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

    customers = [{
        'index': row[0], 
        'transaction_date': row[1], 
        'transaction_name': row[2], 
        'transaction_reference_number': row[3],
        'value_date': row[4],
        'withdrawn_amount': row[5],
        'deposit_amount': row[6],
        'closing_balance': row[7],
        } for row in rows]
    return JsonResponse({'transactions': customers})



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
        # response = chain.invoke({"question": "You are an SQL expert, you are working with postgres database, you are given a database that contains the customers bank spending document. Give me all the distinct transactions that was done towards swiggy. Show the list without any Limit. Also while you're retrieving the documents, keep in mind that the transactions can be described in upper case or lower case. "})
        response = chain.invoke({"question": "You are an SQL expert, you are working with postgres database, you are given a database that contains the customers bank spending document. Give me data for monthly expences for each month. Show the list without any Limit. Also while you're retrieving the documents, keep in mind that the transactions can be described in upper case or lower case. "})
        
        print("monthly expences", response)
        # cursor.execute("SELECT * FROM uploads_transaction")
        cursor.execute("SELECT DISTINCT t.reference_number FROM uploads_transaction t WHERE t.transaction_name LIKE '%swiggy%'")
        # cursor.execute(response)
        rows = cursor.fetchall()
        output = db.run(response)

    # toutput = [{'name': row[0], 'email': row[1], 'created_at': row[2]} for row in output]

    customers = [{'name': row[0], 'email': row[1], 'created_at': row[2]} for row in rows]
    return JsonResponse({'output': output, 'customers': customers, 'query':response})


class DocumentListView(generics.ListAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    
    queryset = UploadedFile.objects.all()
    serializer_class = DocumentSerializer


class DocumentDetailView(APIView):
    def get(self, request, document_id, format=None):
        try:
            document = UploadedFile.objects.get(id=document_id)
            documentserializer = DocumentSerializer(document)

            if document.user == request.user:
                transaction = Transaction.objects.filter(document_id=document_id, user_id=request.user)
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

class QueryAnalysis(BaseModel):
    query_type: Optional[str] = Field(description="The type of query, e.g., 'average_balance', 'total_spending', etc.", default=None)
    chart_type: Optional[str] = Field(description="The type of chart to display, e.g., 'bar', 'line', 'table', etc.", default=None)
    time_range: Optional[int] = Field(description="The time range in months for the query", default=None)
    sql_query: Optional[str] = Field(description="The SQL query to execute", default=None)

# note: keep the database separate from the main user database, since LLM will get access to all the database
#  and users and ask any questions to access the main database
# class ChatWithRag(APIView):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.llm = llm
#         self.query_analyzer = self.create_query_analyzer()
#         self.sql_generator = self.create_sql_generator()
#         self.answer_prompt = self.create_answer_prompt()

#     def create_answer_prompt(self):
#         answer_prompt = PromptTemplate.from_template(
#             """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

#         Question: {question}
#         SQL Query: {sql_query}
#         SQL Result: {sql_result}
#         Answer: """
#         )

#         return answer_prompt

#     def create_sql_generator(self):
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", """You are a PostgreSQL expert. Generate a SQL query to answer this question: {message}

#             Guidelines:
#             1. Use only PostgreSQL-compatible syntax.
#             2. Wrap the entire query in a SELECT statement that returns a JSON object:
#                SELECT json_build_object('data', (your_query_here)) AS result
#             3. Use json_agg and json_build_object in the outer query to structure the result.
#             4. Cast all numeric and date values to VARCHAR using CAST(... AS VARCHAR).
#             5. Don't use LIMIT unless specifically asked.
#             6. Handle upper and lower case in string comparisons using LOWER() function.
#             7. Use date_trunc('month', date_column) for monthly aggregations.
#             8. For complex queries, use WITH clauses for better readability.
#             9. Avoid nested aggregate functions. Use subqueries or subselects instead.
#             10. Always test your query structure to ensure it's valid.
#             11. Do not include any explanations or notes, just the SQL query.
#             12. Do not include a semicolon at the end of the query.
#             13. For recurring transactions, consider transactions with the same name occurring in multiple months.

#             The database has a table 'uploads_transaction' with columns: 
#             id, document_id, transaction_date, transaction_name, withdrawn_amount, deposit_amount, reference_number, closing_balance.

#             Now, generate a working PostgreSQL query to answer the question."""),
#             ("human", "{query}"),
#             ("human", "Time range: {time_range} months")
#         ])
        
#         return prompt | self.llm

#     def create_query_analyzer(self):
#         output_parser = PydanticOutputParser(pydantic_object=QueryAnalysis)
        
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", """You are an AI assistant that analyzes user queries about financial data. 
#             Based on the user's query, determine:
#             1. The type of query(query_type) (e.g., average_balance, total_spending, average_withdrawal)
#             2. The type of chart(chart_type) that would best represent this data (bar, line, or table)
#             3. chart_type is only applicable for the following aggregate queries: average, average_withdrawal, debit_credit_category, payment_mode_category, list_transactions, etc
#             4. The time range for the query in months(time_range)
            
#             For example:
#             Example 1:
#             if the user asks "What is the total average spending for the last 6 months?"
#             The query_type would be "total_spending", the chart_type would be "bar", and time_range would be 6.
            
#             Example 2:
#             if the user asks "What is my average monthly balance for the last 6 months?"
#             The query_type would be "average_balance", the chart_type would be "bar", and time_range would be 6.
            
#             Example 3:
#             if the user asks "What is my average monthly withdrawal for the last 6 months?"
#             The query_type would be "average_withdrawal", the chart_type would be "bar", and time_range would be 6.
            
#             Example 4:
#             if the user asks "Categorize my transactions by debit and credit values"    
#             The query_type would be "debit_credit_category", the chart_type would be "pie", and time_range would be None.
             
#             Example 5:
#             if the user asks "Categorise my transactions by mode of payment"
#             The query_type would be "payment_mode_category", the chart_type would be "pie", and time_range would be None.
             
#             Example 6:
#             if the user asks "List all the transactions that were done towards swiggy"
#             The query_type would be "list_transactions", the chart_type would be "table", and time_range would be None.
            
#             Do not generate SQL queries in this step. Respond with a JSON object containing these details."""),
#             ("human", "{query}"),
#             ("human", "Analyze the above query and provide the output in the following format:\n{format_instructions}")
#         ])
        
#         return prompt.partial(format_instructions=output_parser.get_format_instructions()) | self.llm | output_parser

#     # def post(self, request, question_id, format=None):
#     #     user_data = request.data
#     #     user_query = user_data.get('message', '')
#     #     documendId = user_data.get('documentId', '')
        
#     #     # Analyze the query using the LLM
#     #     # analysis = self.query_analyzer.invoke({"query": message})

#     #     # print("analysis", analysis)

#     #     username = "postgres"
#     #     hostname = "localhost"
#     #     database = "mysiteDB"
#     #     port = "5432"
#     #     connection_string = f"postgresql+psycopg2://{username}:{encoded_password}@{hostname}:{port}/{database}"
#     #     # create database connection
#     #     db = SQLDatabase.from_uri(connection_string)

#     #     # Logging db details
#     #     # print("dialect", db.dialect)
#     #     # print("table names", db.get_usable_table_names())
#     #     # print("table info", db.table_info)

#     #     # create chain between your DB and LLM
#     #     generate_query = create_sql_query_chain(llm, db)

#     #     # print the default generater prompt
#     #     # chain.get_prompts()[0].pretty_print()
        
#     #     try:
#     #         # invoke chain to generate the SQL query
#     #         # sql_query = generate_query.invoke({"question": user_query})

#     #         # print("query", sql_query)

#     #         # Execute the returned query directly
#     #         # output = db.run(sql_query)

#     #         # print("output", output)

#     #         # Execute the returned query using chain
#     #         execute_query = QuerySQLDataBaseTool(db=db)

#     #         chain = generate_query | execute_query

#     #         # invoke chain to generate and execute SQL query and get output
#     #         # response = chain.invoke({"question": user_query})

#     #         #  To show the response in a more user friendly way.

#     #         #  1. create an answer prompt, chain the generate prompt with llm, and parse the output as string 
#     #         #  answer chain will create prompt from original user question, the generate sql query, and the query executed result
#     #         #  share the prompt to llm to get human readable output
#     #         #  requires  "sql_query", "sql_result" and "user_question"
#     #         answer = self.answer_prompt | llm | StrOutputParser()


#     #         # 2. create chain to assign the result of generate_query to the 'sql_query' key
#     #         # . and assign the result of (sql_query | execute_query) to the 'sql_result' key
#     #         # . chain the assigned sql_query and sql_result to answer chain to get human readable form output 
#     #         chain = (
#     #             RunnablePassthrough.assign(sql_query=generate_query).assign(
#     #                 sql_result=itemgetter("sql_query") | execute_query
#     #             )
#     #             | answer
#     #         )

#     #         # 3. finally execute the chain with the user_query
#     #         # note: can keep the "question" to something else like "user_question", cause we are using langchain tools
#     #         # for generating and executing query, and it expects "question" key
#     #         response = chain.invoke({"question": user_query})

#     #         # response = chain.invoke({
#     #         #     "question": f"""
#     #         #     You are a PostgreSQL expert. Generate a SQL query to answer this question: {message}

#     #         #     Guidelines:
#     #         #     1. Use only PostgreSQL-compatible syntax.
#     #         #     2. Wrap the entire query in a SELECT statement that returns a JSON object:
#     #         #        SELECT json_build_object('data', (your_query_here)) AS result
#     #         #     3. Use json_agg and json_build_object in the outer query to structure the result.
#     #         #     4. Cast all numeric and date values to VARCHAR using CAST(... AS VARCHAR).
#     #         #     5. Don't use LIMIT unless specifically asked.
#     #         #     6. Handle upper and lower case in string comparisons using LOWER() function.
#     #         #     7. Use date_trunc('month', date_column) for monthly aggregations.
#     #         #     8. For complex queries, use WITH clauses for better readability.
#     #         #     9. Avoid nested aggregate functions. Use subqueries or subselects instead.
#     #         #     10. Always test your query structure to ensure it's valid.
#     #         #     11. Do not include any explanations or notes, just the SQL query.
#     #         #     12. Do not include a semicolon at the end of the query.
#     #         #     13. For recurring transactions, consider transactions with the same name occurring in multiple months.


#     #         #     Now, generate a working PostgreSQL query to answer the question.
#     #         #     """
#     #         # })
            
#     #         # # # Remove any trailing semicolons from the generated query
#     #         # response = response.rstrip(';')
            
#     #         # print("Generated SQL query:", response)
            
#     #         # # Modify the query to always return a JSON array, even if empty
#     #         # modified_query = f"""
#     #         # WITH query_result AS ({response})
#     #         # SELECT COALESCE(json_agg(result), '[]'::json) AS result FROM query_result
#     #         # """
            
#     #         # output = db.run(modified_query)
#     #         # # print("output", output)
#     #         # # print("output1", output[0])
#     #         # # print("output type:", type(output))
#     #         # # print("output[0] type:", type(output[0]) if output else "N/A")
#     #         # # print("output[0][0] type:", type(output[0][0]) if output and output[0] else "N/A")

#     #         # # Convert string to Python data structure
#     #         # parsed_output = ast.literal_eval(output)

#     #         # # Extract the data value
#     #         # data_value = parsed_output[0][0][0]['data']
#     #         # # print("data_value", data_value)
#     #         # # Parse the output safely
#     #         # # if output and output[0] and output[0][0]:
#     #         # #     json_data = output[0][0]
#     #         # #     if isinstance(json_data, str):
#     #         # #         try:
#     #         # #             json_dict = json.loads(json_data)
#     #         # #         except json.JSONDecodeError:
#     #         # #             json_dict = []
#     #         # #     else:
#     #         # #         json_dict = json_data
#     #         # # else:
#     #         # #     json_dict = []

#     #         response_data = {
#     #             'output': user_query,
#     #             'response': 'Query executed successfully.',
#     #             # 'message': data_value,
#     #             'message': response,
#     #             'sender': 'admin',
#     #             # 'query_type': analysis.query_type,
#     #             # 'chart_type': analysis.chart_type,
#     #             # 'time_range': analysis.time_range,
#     #             'query_type': response,
#     #             'chart_type':response,
#     #             'time_range': response,
#     #             # 'sql_query': response
#     #             'sql_query': response
#     #         }
#     #         return Response(response_data, status=200)
            
#     #     except Exception as e:
#     #         error_message = str(e)
#     #         print(f"Error executing query: {error_message}")
#     #         print(f"Raw output: {response}")
            
#     #         response_data = {
#     #             'output': user_query,
#     #             'response': 'An error occurred while processing your request.',
#     #             'error': error_message,
#     #             'sender': 'admin'
#     #         }
#     #         return Response(response_data, status=400)
        




# class ChatWithAgent(APIView):

#     def create_workflow(self) -> StateGraph:
#         """ create and confifure the workflow graph"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_sql_agent(request, document_name) -> dict:
    """ Run the Sql agent worlflow and return the formated answer and visualisation recommendation"""
    # app = self.create_workflow().compile()
    # result = app.invoke({'question': question, "documentid": documentId})
    user_data = request.data
    question = user_data.get('message', '')
    documendId = user_data.get('documentId', '')
    # logger.error(question, documendId, document_name)
    try:
        result = WorkFlowManager.WorkflowManager().run_sql_agent(question=question, uuid=document_name)
        # print(result)
        output = {
            "message": result["answer"],
            "visualization": result['visualization'],
            "visualization_reason": result['visualization_reason'],
            "formated_data_for_visualization": result['formatted_data_for_visualization'],
            'sender': 'admin',
            'complete': result,
        }
        return JsonResponse({'success': True, 'data': output}, status=200)
    except Exception as e:
        error_msg = "Failed to analyse your request"
        return JsonResponse({'success': False, 'errors': error_msg}, status=400)
