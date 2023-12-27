from django.shortcuts import render
from blogs.models import Blog
from client.models import Client
from mailing.models import Mailing


#def blog_list(request):
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
    return render(request, 'blogs/blog_list.html', context)
