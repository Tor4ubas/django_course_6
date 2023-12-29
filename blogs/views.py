from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from blogs.forms import BlogForm
from blogs.models import Blog
from client.models import Client
from mailing.models import Mailing


# def blog_list(request):
#    blogs = Blog.objects.filter(is_published=True).order_by('?')[:3]
#    count_mailing = Mailing.objects.count()
#    count_active_mailing = Mailing.objects.filter(status=2).count()
#    unique_clients = Mailing.objects.values('user_id').distinct().count()

#    context = {
#        'blogs': blogs,
#        'count_mailing': count_mailing,
#        'count_active_mailing': count_active_mailing,
#        'unique_clients': unique_clients,

#    }
#    return render(request, 'blogs/blog_list.html', context)
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog_list.html')
    else:
        form = BlogForm()
    return render(request, 'blogs/blog_form.html', {'form': form})


def view_blog_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.count_views += 1
    post.save()
    return render(request, 'blogs/blog_detail.html', {'object': post})


def list_blog_posts(request):
    blog = Blog.objects.filter(is_published=True).order_by('?')
    context = {
        'blog': blog,

    }
    #posts_without_slug = posts.filter(slug__isnull=True)
    #posts_without_slug.delete()
    return render(request, 'blogs/blog_list.html', context)


def update_blog_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        header = request.POST.get('header')
        content = request.POST.get('content')
        is_published = request.POST.get('is_published')
        post.header = header
        post.content = content
        post.is_published = is_published
        post.save()
        return redirect(reverse('blogs:update_post', args=[pk]))
    return render(request, 'blogs/blog_form.html', {'post': post})


def delete_blog_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect(reverse('blogs:blogs'))
    return render(request, 'blogs/blog_confirm_delete.html', {'post': post})


def main(request):
    client = len(Client.objects.all().distinct('email'))
    blog = Blog.objects.filter(is_published=True).order_by('?')
    mailing = len(Mailing.objects.all())
    mailing_active = len(Mailing.objects.filter(status=2))
    context = {
        'blog': blog[:3],
        'mailing': mailing,
        'mailing_active': mailing_active,
        'client': client
    }
    return render(request, 'blogs/main.html', context)
