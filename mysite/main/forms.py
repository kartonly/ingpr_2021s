from .models import News
from django.forms import ModelForm, TextInput, Textarea


class NewsForm(ModelForm):
    class Meta:
        model=News
        fields=["Title", "About"]
        widgets = {"Title": TextInput(attrs={'class':'form-control', 'placeholder':'Название новости', 'id':'name'}),
                   "About": Textarea(attrs={'class':'form-control', 'placeholder':'Сама новость', 'id':'text'})
                   }
