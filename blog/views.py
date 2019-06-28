from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, reverse
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Blog
from .forms import ContactForm, BlogForm, PostSorguForm, CommentForm


# Create your views here.

mesajlar= []

def iletisim(request) :
    form = ContactForm(data=request.GET or None)
    if form.is_valid():
        isim = form.cleaned_data.get('isim')
        soyisim = form.cleaned_data.get('soyisim')
        email = form.cleaned_data.get('email')
        icerik = form.cleaned_data.get('icerik')
        data = {'isim': isim, 'soyisim': soyisim, 'email': email, 'icerik': icerik}
        mesajlar.append(data)
        return render(request, 'iletisim.html', context={'mesajlar': mesajlar, 'form': form})

    return render(request, 'iletisim.html', context={'form': form})

def posts_list(request):
    posts = Blog.objects.all()
    page = request.GET.get('page', 1)
    form = PostSorguForm(data=request.GET or None)
    if form.is_valid():
        taslak_yayin = form.cleaned_data.get('taslak_yayin', None)
        search = form.cleaned_data.get('search', None)
        if search:
            posts = posts.filter(Q(content__icontains=search)|Q(title__icontains=search)|Q(kategoriler__isim__icontains=search)).distinct()
        if taslak_yayin and taslak_yayin != 'all':
         posts = posts.filter(yayin_taslak=taslak_yayin)

    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {'posts': posts, 'form': form}
    return render(request, 'blog/post-list.html', context)

def post_update(request, slug):
    blog = get_object_or_404(Blog, slug = slug )
    form = BlogForm(instance=blog,data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        msg = 'Tebrikler <strong> %s </strong> isimli gönderiniz başarıyla güncellendi.' % (blog.title)
        messages.success(request, msg, extra_tags='info')
        return HttpResponseRedirect(reverse('post-detail',kwargs={'slug': blog.slug}))
    context = {'form': form, 'blog': blog}
    return render(request, 'blog/post-update.html', context=context)

def post_delete(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    blog.delete()
    msg = '<strong> %s </strong> isimli gönderiniz silindi.' % (blog.title)
    messages.success(request, msg, extra_tags='danger')
    return HttpResponseRedirect(reverse('post-list'))

def post_detail (request, slug):
    form = CommentForm()
    blog = get_object_or_404(Blog, slug=slug)
    blog.get_blog_comment()
    return render(request, 'blog/post-detail.html', context={'blog':blog, 'form':form})

def add_comment(request, slug):
    if request.method == 'GET':
        return HttpResponseBadRequest()
    blog = get_object_or_404(Blog, slug=slug)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.blog = blog
        new_comment.save()
        messages.success(request, 'Tebrikler yorumunuz başarıyla oluşturuldu.')
        return HttpResponseRedirect(blog.get_absolute_url())


def post_create(request):
    form = BlogForm()
    if request.method == 'POST':
        print(request.FILES)
        form = BlogForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blog = form.save()
            msg = 'Tebrikler <strong> %s </strong> isimli gönderiniz başarıyla oluşturuldu.' %(blog.title)
            messages.success(request, msg, extra_tags='success')
            return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': blog.slug}))
    return render(request, 'blog/post-create.html',context={'form': form})

def sanatcilar(request, sayi):
    sanatcilar_sozluk = {

        '1': 'Pink Floyd',
        '2': 'Şebnem Ferah',
        '3': 'Hayko Cepkin',
        '4': 'Metallica',
        '5': 'Iron Maiden',
        '6': 'Mor ve Ötesi',
    }

    sanatci = sanatcilar_sozluk.get(sayi, "Bu id numarasına ait sanatci bulunamadi.")
    return HttpResponse(sanatci)