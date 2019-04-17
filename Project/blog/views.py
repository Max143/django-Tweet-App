from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # Class-based Views
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User


# No Longer Need this dummy data so uncommenting below
'''
posts = [
	{
		'author': 'CoreyMS', 
		'title' : 'Blog Post 1',
		'content' : 'First post content',
		'date_posted': 'August 27, 2019'

	}, 
	{
		'author': 'jane Doe', 
		'title' : 'Blog Post 2',
		'content' : 'Second post content',
		'date_posted': 'jan 14, 2019'

	}
]

'''  
def show(request):
	return render(request, 'blog/show.html')

@login_required																																		
def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)


class PostListView(LoginRequiredMixin, ListView):
	model = Post  # what model to query to create List
	template_name = 'blog/home.html' 
	# By default, Our ListView is going  to call thaat variable  'post in hone function above
	# as a object_list instead of post, 
	# To change that 
	context_object_name = 'posts'   	# By default is posts
	ordering = ['-date_posted']
	paginate_by = 4


class UserPostListView(LoginRequiredMixin, ListView):
	model = Post  # what model to query to create List
	template_name = 'blog/user_post.html'
	context_object_name = 'posts'   	# By default is posts
	ordering = ['-date_posted']
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user # self.request.user is current logged in users
		return super().form_valid(form) # form_valid here is running with supper class
	'''
	Cannot assign "<SimpleLazyObject: <django.contrib.auth.models.
	AnonymousUser object at 0x00000162E6EF95F8>>": 
	"Post.author" must be a "User" instance

	or Integrity Error -
	NOT NULL constraint falied: blog_post.author.id  

	Means no author instance. 
	'''


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		# Getting exact post which we are updating 
		post = self.get_object()  
		if self.request.user == post.author:
			return True
		else:
			return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post 
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
	
	


def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})