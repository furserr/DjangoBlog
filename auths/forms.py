from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=5, required=True, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(min_length=5, required=True, label='Password Confirm', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields=['first_name','last_name','username','email','password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['first_name'].required= True
        self.fields['last_name'].required= True

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password', 'Parolalar Eşleşmedi')
            self.add_error('password_confirm', 'Parolalar Eşleşmedi')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email zaten kayıtlı.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu kullanıcı adı zaten alınmış.')
        return username