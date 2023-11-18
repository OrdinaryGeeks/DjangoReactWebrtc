from django.db import models

# Create your models here.


class Student(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    studentName = models.CharField(max_length=30, null=True, blank=True)
    connectionID = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.studentName + self.connectionID