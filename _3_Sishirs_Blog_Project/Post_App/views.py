from django.shortcuts import redirect, render
from Categories_App.models import Categories
from .models import *
from .helper import *
from Comment_App.models import *
from django.contrib.auth.models import User

def home(request):
    context = {
        'top_post' : get_most_viewed_post(),
        'title_text' : 'Posts',
        'categories' : Categories.objects.all(),
        'posts' : get_post_by_page(1), 
        'post_count' : Post.objects.all().count(),
        'prev_page' : 0,
        'cur_page' : 1,
        'next_page' : 2,
    }
    print(context['post_count'])

    if request.user.is_authenticated:
        return render(request, 'authenticated_home.html', context)
    
    return render(request, 'authenticated_home.html', context)
    # return render(request, 'home.html', context)


def view_post_by_category(request, slug):
    top_post = get_most_viewed_post()
    category = Categories.objects.get(slug=slug)
    context = {
        'top_post' : top_post,
        'title_text' : f' {category.name} Categories Posts',
        'categories' : Categories.objects.all(),
        'posts' : Post.objects.filter(categories = category),
    }

    # if request.user.is_authenticated:
    #     return render(request, 'authenticated_home.html', context)
    
    # return redirect('home')
    return render(request, 'authenticated_home.html', context)

def add_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'Categories': Categories.objects.all(),
    }

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_ids = request.POST.getlist('categories')  # getlist for ManyToMany field
        author = request.user  # Directly using the User object, not the ID

        # Ensure that the post with the same title doesn't exist
        if not Post.objects.filter(title=title).exists():
            post = Post(title=title, author=author, content=content)

            # Save content to a text file using the set_content method
            # post.set_content(content)

            # Add categories to the ManyToMany field after saving the post
            post.save()  # Save the Post object first
            post.categories.add(*category_ids)  # Unpack the category IDs list

        return redirect('viewpost', url=post.slug_url)

    return render(request, 'add_post.html', context)

def home_post_by_page(request, page_no):
    context = {
        'top_post' : get_most_viewed_post(),
        'title_text' : 'Posts',
        'categories' : Categories.objects.all(),
        'posts' : get_post_by_page(page_no), 
        'post_count' : Post.objects.all().count(),
        'prev_page' : page_no - 1,
        'cur_page' : page_no,
        'next_page' : page_no + 1,
    }
    if context['cur_page'] * 8 >= context['post_count']:
        context['next_page'] = None

    print(context['post_count'])
    return render(request, 'authenticated_home.html', context)


from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
def view_post(request, url):
    try:
        post = get_object_or_404(Post, slug_url=url)
    except Http404:
        return redirect('home')
    
    post.views += 1
    post.save()

    comments = post.comments.all().order_by('-id')
    context = {
        'post' : post,
        'comments' : comments,
    }

    if request.method == 'POST':
        text = request.POST.get('comment')
        
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            comment_text=text
        )
        comment.save()
    return render(request, 'view_post.html', context)

def edit_post(request, slug_url):
    post = get_object_or_404(Post, slug_url=slug_url)

    if not request.user.is_authenticated or post.author != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.categories.set(request.POST.getlist('categories'))
        post.save()
        return redirect('viewpost', url=post.slug_url)
    
    context = {
        'post': post,
        'content': post.content,
        'Categories' : Categories.objects.all(),
    }
    return render(request, 'edit_post.html', context)

def delete_post(request, slug_url):
    post = Post.objects.get(slug_url=slug_url)
    if not request.user.is_authenticated or post.author != request.user:
        return redirect('viewpost', url = post.slug_url)

    post.delete()
    return redirect('home')