from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    image=models.ImageField(upload_to='static/dist')
    def __str__(self):
        return self.name
    

class Book(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', default=1)  
    book_id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=2000)
    Author=models.CharField(max_length=2000)  
    tags=models.CharField(max_length=100)
    image=models.ImageField(upload_to='static/dist')
    book=models.FileField(upload_to='static/dist')
    Description=models.TextField()  
    pdf_file = models.FileField(upload_to='static/dist')
        
    def __str__(self):
        return self.name

 


