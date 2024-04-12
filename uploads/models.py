from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploadsDIR/')

    def __str__(self):
        return self.file.name
