from django.urls import path

from .views import upload_file, index

urlpatterns = [
    # ex: /uploads/
    path("<int:question_id>", index, name="index"),
    path('upload/', upload_file, name='file-upload'),

]

