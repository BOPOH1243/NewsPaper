from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Create your views here.
from .models import *
from .filters import NewsFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail

class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'

    def get_success_url(self):
        post = self.object
        print(post)
        subscribers = post.post_subscribers()
        print(subscribers)
        send_mail(
            subject=f'новый пост по подписке{post.header}',
            message = f'{post.preview(length=50)}',
            from_email='djangotestmail1337@gmail.com',
            recipient_list=[i.email for i in subscribers]
        )
        return super().get_success_url()




def create_new(request):
    form = PostForm()
    if request.method =='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    return render(request, 'new_edit.html', {'form':form})


class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'

class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')