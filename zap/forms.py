from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from .models import Meep, Profile


class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile picture')
    profile_bio = forms.CharField(label='', required=False,
                             widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your bio here'}))
    homepage_link = forms.CharField(label='', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website link'}))
    facebook_link = forms.CharField(label='', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook link'}))
    instagram_link = forms.CharField(label='', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instagram link'}))
    linkedin_link = forms.CharField(label='', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Linkedin link'}))

    class Meta:
        model = Profile
        fields = ['profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link']


class MeepForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   'placeholder':'Enter your Social Meep!',
                                   'class':'form-control',
                               }
                               ),
                               label='',
                           )
    class Meta:
        model = Meep
        exclude = ['user','likes']


class SignUpForm(UserCreationForm):#UserCreationForm
    email = forms.EmailField(label='',
                             widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E-mail address'}))
    first_name = forms.CharField(label='', max_length=50,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model= User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class ="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to other personal information.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'



class UpdateForm(UserChangeForm):#UserCreationForm
    email = forms.EmailField(label='',
                             widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E-mail address'}))
    first_name = forms.CharField(label='', max_length=50,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model= User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = '<span class ="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password'].label = ''