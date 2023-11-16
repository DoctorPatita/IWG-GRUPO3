from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from blog.models import BlogPost, Comment
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm, AddCommentForm
from account.models import Usuario
from organization.models import Member, Organization

BLOG_POSTS_PER_PAGE = 10

# Create your views here.

def create_blog_view(request):

	request.POST._mutable = True

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')
	
	members = Member.objects.filter(user=request.user.username)
	all_organizations = Organization.objects.all()

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if request.POST.get('organization', False) == 'Seleccione una organización':
		request.POST['organization'] = Organization.objects.filter(name='Sin organización asociada').first()
	else:
		request.POST['organization'] = Organization.objects.filter(name=request.POST.get('organization', False)).first()
		print(request.POST['organization'])
	if form.is_valid():
		obj = form.save(commit=False)
		author = Usuario.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()
		return redirect('home')

	context['form'] = form
	context['members'] = members
	context['all_organizations'] = all_organizations

	return render(request, 'blog/create_blog.html', context)

def detail_blog_view(request, slug):
	
	context = {}
	blog_post = get_object_or_404(BlogPost, slug=slug)
	num_comments = Comment.objects.filter(post=blog_post).count()
	context['blog_post'] = blog_post
	context['num_comments'] = num_comments

	#copia de home_sreen_view, porque no se puede importar por error de importación circular
		#Barra de busqueda
	query = ""
	if request.GET:
		context = {}
		query = request.GET.get('q', '')
		context['query'] = str(query)

		blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)

	# Pagination
		page = request.GET.get('page', 1)
		blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
		try:
			blog_posts = blog_posts_paginator.page(page)
		except PageNotAnInteger:
			blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
		except EmptyPage:
			blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

		context['blog_posts'] = blog_posts

		return render(request, "personal/home.html", context)
	#final de copia de home_sreen_view

	return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):
	
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse("No eres el dueño de este blog!")

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Actualizado"
			blog_post = obj
	
	form = UpdateBlogPostForm(
			initial={
					"title": blog_post.title, 
					"body": blog_post.body,
					"image": blog_post.image,
				}
			)
	context['form'] = form

	return render(request, 'blog/edit_blog.html', context)

def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		posts = BlogPost.objects.filter(
			Q(title__icontains=q)|
			Q(body__icontains=q)
			).distinct()
		for post in posts:
			queryset.append(post)

	# Crear un set unico y luego convertirlo a una lista
	return list(set(queryset)) 

def add_comment(request, slug):

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	blog_post = get_object_or_404(BlogPost, slug=slug)

	form = AddCommentForm(instance=blog_post)
	if request.method == "POST":
		form = AddCommentForm(request.POST, instance=blog_post)
		if form.is_valid():
			name = request.user.username
			body = form.cleaned_data['body']
			c = Comment(post=blog_post, name=name, body=body)
			c.save()
			return redirect("http://127.0.0.1:8000/blog/"+slug)
	
	else:
		form = AddCommentForm()

	context = {
		'form' : form
	}

	return render(request, 'blog/add_comment.html', context)

def delete_comment(request, slug):
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')
	
	blog_post = get_object_or_404(BlogPost, slug=slug)
	comment = Comment.objects.filter(post=blog_post).last()
	comment.delete()
	return redirect("http://127.0.0.1:8000/blog/"+slug)


