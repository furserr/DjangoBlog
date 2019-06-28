from django.db import models
from django.shortcuts import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify
from uuid import uuid4
import os
from ckeditor.fields import RichTextField


def upload_to(instance, filename):
    uzanti = filename.split(',')[-1]
    new_name = '%s.%s' % (str(uuid4()), uzanti)
    unique_id = instance.unique_id
    return os.path.join('blog', unique_id, new_name)

class Kategori(models.Model):
    isim = models.CharField(max_length=10, verbose_name='Kategori İsim')

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.isim

class Blog(models.Model):

    YAYIN_TASLAK = ((None, 'Seçiniz'), ('yayin', 'YAYIN'), ('taslak', 'TASLAK'))

    title = models.CharField(max_length=100, blank= False, null=True, verbose_name='Başlık Giriniz',help_text='Başlık Bilgisi Burada Girilir.')

    content = RichTextField(max_length=1000,verbose_name='İçerik Giriniz', null= True)

    slug = models.SlugField(null=True, unique=True, editable=False)

    image = models.ImageField(default='default/wall.png', upload_to=upload_to, verbose_name='Resim', null=True, blank=True, help_text='Kapak fotoğrafı yükleyiniz')

    yayin_taslak = models.CharField(choices=YAYIN_TASLAK, max_length=6, null=True, blank=False)

    unique_id = models.CharField(max_length=100, editable=False, null=True)

    kategoriler = models.ManyToManyField(to=Kategori, related_name='blog')

    created_date = models.DateField(auto_now_add=True,auto_now=False)

    class Meta :
        verbose_name_plural = 'Gönderiler'
        ordering = ['id']

    def __str__(self):
        return "%s" %(self.title)

    def get_yayin_taslak_html(self):
        if self.yayin_taslak == 'taslak':
            return '<span class="label label-{1}">{0}</span>'.format(self.get_yayin_taslak_display(), 'danger')
        return '<span class="label label-{1}">{0}</span>'.format(self.get_yayin_taslak_display(), 'success')

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/media/default/wall.png'


    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title))
        new_slug = slug
        while Blog.objects.filter(slug=new_slug).exists():
            sayi += 1
            new_slug = "%s-%s" % (slug, sayi)

        slug=new_slug
        return slug


    def save(self, *args, **kwargs):
        if self.id is None:
            new_unique_id = str(uuid4())
            self.unique_id = new_unique_id
            self.slug = self.get_unique_slug()
        else:
            blog = Blog.objects.get(slug=self.slug)
            if blog.title != self.title:
                self.slug = self.get_unique_slug()
        super(Blog, self).save(*args, **kwargs)

    def get_blog_comment(self):
        #gönderiye ait tüm yorumları veren fonksiyon
        return self.comment.all()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, null=True, related_name='comment')
    isim = models.CharField(max_length=20, blank=True, null=True, verbose_name='İsim')
    soyisim = models.CharField(max_length=20,blank=True,null=True,verbose_name='Soyisim')
    email = models.EmailField(blank=True,null=True,verbose_name='Email', help_text='Bu alan zorunlu.')
    icerik = RichTextField(max_length=1000,blank=False,null=True,verbose_name='Yorum', help_text='Yorum yazınız.')
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        return "%s%s"%(self.email,self.blog)

    def get_screen_name(self):
        if self.isim:
            return "%s%s" % (self.isim, self.soyisim)
        return self.email