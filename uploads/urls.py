from django.urls import path
from .views import upload_file, index, upload_and_parse_file

urlpatterns = [
    # ex: /uploads/
    path("<int:question_id>", index, name="index"),
    path('upload', upload_file, name='file-upload'),
    path('uploadxls', upload_and_parse_file, name='upload-xls'),
]

