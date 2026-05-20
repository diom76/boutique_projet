from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['client_nom','client_email','quantite']
        Widget = {
            'client_nom': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Votre nom'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder':'Votre email'
            }),
            'quantite': forms.NumberInput(attrs={
                'class':'form-control',
                'min':'1'
            }),
        }
class ContactForm(forms.Form):
    nom  = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder' :'Votre nom'
        })
    )        
    email =forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class' : 'from-control',
            'placeholder' : 'Votre email'
        })
    )
    sujet =forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sujet de votre message'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows':5,
            'placeholder':'Votre message...'
        })
    )
    
    def clea_message(self):
        message= self.cleaned_data['message']
        if len(message)<10:
            raise forms.ValidationError('Le message doit contenir au moins 10 caracteres.')
        return message