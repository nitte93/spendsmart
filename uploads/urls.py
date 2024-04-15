from django.urls import path
from .views import upload_file, index,chat,ChatWithRag, upload_and_parse_file, list_customers_raw, DocumentListView,DocumentDetailView

urlpatterns = [
    # ex: /uploads/
    path("<int:question_id>", index, name="index"),
    path("chat/<int:question_id>", chat, name="chat"),
    path("chatwithrag/<int:question_id>", ChatWithRag.as_view(), name="ChatWithRag"),
    path('upload', upload_file, name='file-upload'),
    path('uploadxls', upload_and_parse_file, name='upload-xls'),
    path('transactions', list_customers_raw, name='get-transactions'),
    path('documents', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:document_id>', DocumentDetailView.as_view(), name='document-id'),
]

