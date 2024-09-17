from django.urls import path
from .views import upload_file, index,chat, list_customers_raw,read_db_content, run_sql_agent, DocumentListView,DocumentDetailView, upload_and_parse_excel_to_sql

urlpatterns = [
    # ex: /uploads/
    path("<int:question_id>", index, name="index"),
    path("chat/<str:document_name>", chat, name="chat"),
    # path("chatwithrag/<int:question_id>", ChatWithRag.as_view(), name="ChatWithRag"),
    path("chatwithrag/<str:document_name>", run_sql_agent, name="ChatWithRag"),
    path('upload', upload_file, name='file-upload'),
    # path('uploadxls', upload_and_parse_file, name='upload-xls'),
    path('upload-file', upload_and_parse_excel_to_sql, name='upload-file'),
    path('transactions', list_customers_raw, name='get-transactions'),
    path('transaction-list', read_db_content, name='list-transactions'),
    path('documents', DocumentListView.as_view(), name='document-list'),
    # path('documents/<int:document_id>', DocumentDetailView.as_view(), name='document-id'),
    path('documents/<str:document_name>', read_db_content, name='document_name'),
]

