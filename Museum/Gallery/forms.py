from django import forms
from django.forms import Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Gallery.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ClearableFileInput, Select, ModelForm, DateTimeInput, Textarea, CharField, TextInput, Select, NumberInput, PasswordInput, FileInput, FileField


class ExhibitionForm(ModelForm):
    class Meta:
        model = Exhibition
        fields = ['title', 'description', 'date_and_time']
        widgets = {'title': TextInput(attrs={
            'placeholder': 'title',
            'required': True
            }),
            'description': Textarea(attrs={
                'placeholder': 'description',
                'required': True
            }),
            'date_and_time': DateTimeInput(
                                attrs={
                                    'placeholder': '31/01/2022 11:11',
                                    'format': '%d/%m/%Y %H:%M',
                                    'required': True
                                })
            # 'images': FileField(widget=forms.ClearableFileInput(attrs={
            #     'multiple': True,
            #     'placeholder': 'images',
            #     'required': False
            # }))
        }

class Exhibition_museum_pieceForm(ModelForm):
    class Meta:
        model = Exhibition_museum_piece
        fields = ['museum_piece_id']
        widgets = {
            'museum_piece_id': Select(attrs={
                'required': False
            })
        }

class Museum_pieceForm(ModelForm):
    class Meta:
        model = Museum_piece
        fields = ['piece_name', 'description', 'date_of_creation', 'piece_type', 'author_id', 'hall_id']
        widgets = {'piece_name': TextInput(attrs={
            'placeholder': 'piece_name',
            'required': True
            }),
            'description': Textarea(attrs={
                'placeholder': 'description',
                'required': True
            }),
            'date_of_creation': DateTimeInput( attrs={
                    'placeholder': '31/01/2022 11:11',
                    # 'format': '%d/%m/%Y %H:%M',
                    'required': True
            }),
            'piece_type': TextInput(attrs={
                'placeholder': 'type',
                'required': True
            }),
            'author_id': Select(attrs={
                'required': False,
            }),
            'hall_id': Select(attrs={
                'required': True
            })
            # 'images': FileField(widget=forms.ClearableFileInput(attrs={
            #     'multiple': True,
            #     'placeholder': 'images',
            #     'required': False
            # }))
        }


class ImagesForm(ModelForm):
    class Meta:
        model = Images
        fields = ['image']
        widgets = {'image': ClearableFileInput(
                    attrs={
                        'multiple': True,
                        'placeholder': 'images',
                        'required': False
                    })}


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['full_name']
        widgets = {'full_name': TextInput(attrs={
            'placeholder': 'full name',
            'required': True
            })
        }

class HallForm(ModelForm):
    class Meta:
        model = Hall
        fields = ['hall_number', 'title']
        widgets = {'hall_number': TextInput(attrs={
            'class': 'form_input',
            'placeholder': 'hall number',
            'required': True
            }),
            'title': TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'title',
                'required': False
            })
        }

