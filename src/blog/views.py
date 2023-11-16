from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from blog.models import BlogPost, Comment
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm, CommentForm
from account.models import Usuario




BLOG_POSTS_PER_PAGE = 10

# Create your views here.

def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Usuario.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()

	context['form'] = form

	return render(request, 'blog/create_blog.html', context)

def detail_blog_view(request, slug):
	
	context = {}
	blog_post = get_object_or_404(BlogPost, slug=slug)
	context['blog_post'] = blog_post

	
	#copia home_sreen_view, porque no se puede importar por error de importación circular
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

def add_comment(request, blog_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = BlogPost.objects.get(pk=blog_id)
            comment.author = request.user
            comment.save()
            return redirect('blog:detail', slug=comment.post.slug)  

    
    return render(request, 'blog/comment_form.html', {'form': form})

def ver_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    comments = Comment.objects.filter(post=blog)

    # Verificar si el usuario ha dado like a este blog
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = blog.likes.filter(id=request.user.id).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog
            comment.author = request.user
            comment.save()
            return redirect('blog:ver_blog', blog_id=blog.id)

    return render(request, 'blog/ver_blog.html', {'blog': blog, 'comments': comments, 'user_has_liked': user_has_liked})

def detail_blog_view(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    comments = Comment.objects.filter(post=blog_post)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog_post
            comment.author = request.user
            comment.save()
            return redirect('blog:detail', slug=blog_post.slug)
    else:
        form = CommentForm()
    
    return render(request, 'blog/detail_blog.html', {'blog_post': blog_post, 'comments': comments, 'form': form})

def like_blog_post(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id', None)
        blog = get_object_or_404(BlogPost, id=blog_id)
        user = request.user

        if blog.likes.filter(id=user.id).exists():
            blog.likes.remove(user)
            is_liked = False
        else:
            blog.likes.add(user)
            is_liked = True

        likes_count = blog.likes.count()

        return JsonResponse({'is_liked': is_liked, 'likes_count': likes_count})
    else:
        return HttpResponseBadRequest
    
def like_post(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    blog.likes.add(request.user)
    likes_count = blog.likes.count()
    return JsonResponse({'likes_count': likes_count})