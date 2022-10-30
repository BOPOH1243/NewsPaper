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
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views import View
from django.http import HttpResponse
from .tasks import hello, mail_distributon

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
        if self.request.user.is_anonymous:
            return context
        context['user_subscribes'] = [i.category for i in UserSubscribe.objects.filter(user=self.request.user)]
        return context

class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            return context
        context['user_subscribes'] = [i.category for i in UserSubscribe.objects.filter(user=self.request.user)]  #self.request.user.groups.filter()
        #print(context['user_subscribes'])
        return context

class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'

    def get_success_url(self):
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

@login_required
def subscribe(request,pk):
    user = request.user
    user_subscribes = UserSubscribe.objects.filter(user=user)
    if not pk in [i.category.pk for i in user_subscribes]:
        UserSubscribe.objects.create(user=user,category=Category.objects.get(pk=pk))
    return redirect('/news/')

class TestView(View):
    def get(self, request):
        mail_distributon.delay()
        return HttpResponse('Hello!')