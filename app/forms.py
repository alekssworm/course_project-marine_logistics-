"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)  
    email = forms.EmailField()  

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'company_name', 'first_name', 'last_name', 'email']


from django import forms
from .models import Port, Ship

class EditPortForm(forms.ModelForm):
    class Meta:
        model = Port
        fields = ['port_name', 'port_latitude', 'port_longitude']  # Include the fields you want to be editable

class EditShipForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = ['name_of_vessel', 'ship_tonnage', 'ship_type', 'home_port', 'average_speed','crew']  # Adjust fields as needed

from django import forms
from .models import WritingAContract

class EditContractForm(forms.ModelForm):
    class Meta:
        model = WritingAContract
        fields = ['cargo_quantity', 'type_of_cargo', 'port_id_with_cargo', 'port_final_destination', 'temperature_mode', 'in_work', 'completed']
