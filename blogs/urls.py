from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from blogs import views


from blogs.views import main

app_name = 'blogs'

urlpatterns = [
    path('', main, name='main'),
    path('create/', views.create_blog_post, name='create'),
    path('view/<int:pk>/', views.view_blog_post, name='view'),
    path('blogs/', views.list_blog_posts, name='blogs'),
    path('update/<int:pk>/', views.update_blog_post, name='update'),
    path('delete/<int:pk>/', views.delete_blog_post, name='delete'),
    #path('blogs/', blogs, name='blogs'),
    #path('', blog_list, name='blog_list'),
    #path('blogs/', create_blogpost, name='create'),
    #path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='view'),
    #path('update/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    #path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
