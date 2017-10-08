import time
from django import forms

from expert_app.models_domain import System


class SystemForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Супер-система', }
        ),
        max_length=100,
        label=u'Название'
    )
    slug = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'super-system', }
        ),
        max_length=30,
        label=u'slug (для URL)'
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
        required=False,
        label=u'Доступна всем'
    )

    system = None

    def set_system(self, system):
        self.system = system

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '')
        slugged_system = System.objects.get_by_slug(slug)

        if not slugged_system:
            return slug

        slugged_system = slugged_system.all()[:1].get()

        if self.system is None or slugged_system.id != self.system.id:
            raise forms.ValidationError(u'Такой slug уже занят')

        return slug

    def save(self, user):
        data = self.cleaned_data

        name = data.get('name')
        description = data.get('description')
        author = data.get('author')
        slug = data.get('slug')
        image = data.get('image')
        public = data.get('public')

        if self.system:
            system = self.system
        else:
            system = System()
            system.user = user

        system.name = name
        system.description = description
        system.author = author
        system.slug = slug
        system.public = public

        if image is not None:
            if not image:
                system.image.delete(save=True)
            else:
                system.image.save('%s_%s' % (slug, image.name), image, save=True)

        system.save()

        return system
