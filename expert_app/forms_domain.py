from django import forms


class SystemForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Супер-система', }
        ),
        max_length=100,
        label=u'Название'
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '3', }
        ),
        label=u'Описание'
    )
    author = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Александр Иванник, ИУ5-73', }
        ),
        max_length=100,
        label=u'Авторы'
    )
    image = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control', }),
        required=False, label=u'Изображение'
    )
    public = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control', }
        ),
        label=u'Доступна всем'
    )
