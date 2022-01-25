from django import forms
from .models import Post
from django.template.defaultfilters import filesizeformat
from django.conf import settings

class PostsForm(forms.ModelForm):
    def clean_file(self,form):
        if content != None:
            content = self.cleaned_data['PDFfile']
            content_type = content.content_type.split('/')[1]
            if content_type in settings.CONTENT_TYPES:
                if content._size > int(settings.MAX_UPLOAD_SIZE):
                    raise forms.ValidationError(('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
            else:
                raise forms.ValidationError('Only PDFs are supported!')
    class Meta:
        model=Post
        fields=['title','description','PDFfile','author']
    
