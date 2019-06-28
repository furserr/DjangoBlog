from django import forms
from .models import Blog, Comment


banned_email_list = ['ahmet@gmail.com']

class ContactForm(forms.Form) :
    isim = forms.CharField(max_length=50, label='İsim', required=False)
    soyisim = forms.CharField(max_length=50, label='Soyisim', required=False)
    email = forms.EmailField(max_length=50, label='Email', required=False)
    email2 = forms.EmailField(max_length=50, label='Email', required=True)
    icerik = forms.CharField(widget=forms.Textarea,max_length=50, label='İçerik', required=True)


    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

    def clean_isim(self):
        isim = self.cleaned_data.get('isim')
        if isim == 'ahmet' :
            raise forms.ValidationError('Lütfen Ahmet girmesin')
        return isim

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email in banned_email_list:
            raise forms.ValidationError('Bu email BANNED')
        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email != email2:
            self.add_error('email', 'Emailler Eşleşmedi')
            self.add_error('email2', 'Emailler Eşleşmedi')


class BlogForm(forms.ModelForm):
        class Meta:
            model = Blog
            fields = ['title', 'image', 'content', 'yayin_taslak', 'kategoriler']

        def __init__(self, *args, **kwargs):
            super(BlogForm, self).__init__(*args,**kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['content'].widget.attrs['rows'] = 10

        def clean_content(self):
            icerik = self.cleaned_data.get('content')
            if len(icerik) < 250:
                uzunluk = len(icerik)
                msg= 'Lütfen en az 250 karakter giriniz. Girilen karakter sayısı: (%s)' % (uzunluk)
                raise forms.ValidationError(msg)
            return icerik

class PostSorguForm(forms.Form):
    YAYIN_TASLAK = (('all', 'HEPSİ'), ('yayin', 'YAYIN'), ('taslak', 'TASLAK'))

    search = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'placeholder':'Ara' ,'class':'form-control'}), required=False)

    taslak_yayin = forms.ChoiceField(label='' ,widget=forms.Select(attrs={'class' : 'form-control'}) ,choices=YAYIN_TASLAK, required=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['isim','soyisim','email','icerik']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}