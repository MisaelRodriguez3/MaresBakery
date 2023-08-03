from django import forms

class FormularioContacto(forms.Form):
    nombre = forms.CharField(required=True,
    widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre',
    'class': 'input',}))

    email = forms.CharField(required=True,
    widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su correo',
    'class': 'input',}))

    contenido = forms.CharField(required=True,
    widget=forms.Textarea(attrs={'placeholder': 'Mensaje',
    'class': 'input',}))