from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.
from .models import *


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 3

class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
