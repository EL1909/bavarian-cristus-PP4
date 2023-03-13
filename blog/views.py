from django.shortcuts import render
from django.views import generic
from .models import ImagePost


class PostList(generic.ListView):
    model = ImagePost
    queryset = ImagePost.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6
 