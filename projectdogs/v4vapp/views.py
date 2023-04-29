from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from .models import Post

# from django.http import HttpResponse

# Create your views here.

# def home(request):
#     return HttpResponse('<h1> Home </h1> ')

# def about(request):
#     return HttpResponse('<h1> About </h1> ')


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'v4vapp/home.html',context)

class PostListView(ListView):
    model=Post
    template_name='v4vapp/home.html' # <app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']

class PostDetailView(DetailView):
    model=Post
    template_name='v4vapp/post_detail.html'

class PostCreateView(CreateView):
    model=Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/'
    
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

def about(request):
   
    return render(request,'v4vapp/about.html') 