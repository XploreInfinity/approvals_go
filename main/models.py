from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
#*title is post's title.Description is added by faculty to describe the document(optional)
#*date posted is automatically recorded.PDFfile is the file uploaded by faculty.Author is the faculty who created the post
#*comments are added by HODs if the post gets rejected,suggesting changes.Status defines whether file is 'approved','rejected' or 'pending'
class Post(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(default="No Description",max_length=500)
    date_posted=models.DateTimeField(default=timezone.now)
    PDFfile=models.FileField(upload_to='PDFCollection')
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    comments=models.TextField(default="No Comments",max_length=500)
    status=models.CharField(default='pending',max_length=10)
    
    def __str__(self): #*Returns a specific field value of the object when the object is called
        return self.title
    def get_absolute_url(self):
        return reverse('home')#kwargs={'pk':self.pk()})
