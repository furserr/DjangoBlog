from django.conf.urls import url

from blog.views import post_create, post_delete, post_update, posts_list, sanatcilar, post_detail,add_comment

urlpatterns = [

    url(r'^posts-list/$', posts_list, name='post-list'),
    url(r'^post-create/$', post_create, name='post-create'),
    url(r'^post-detail/(?P<slug>[-\w]+)/$', post_detail, name='post-detail'),
    url(r'^post-update/(?P<slug>[-\w]+)/$', post_update, name='post-update'),
    url(r'^post-delete/(?P<slug>[-\w]+)/$', post_delete, name='post-delete'),
    url(r'^add-comment/(?P<slug>[-\w]+)/$', add_comment, name='add-comment'),
    url(r'^sanatcilar/(?P<sayi>[0-9a-z])/',sanatcilar),


]