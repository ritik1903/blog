from django.http import HttpResponse
from django.shortcuts import render
from Blog.models import Post,Category,Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404


def home(request):
    #load all the post from db(10)
    posts=Post.objects.all()[:11]
    #print(posts)
    cats=Category.objects.all()
    data={
        'posts': posts,
        'cats':cats
    }

    return render(request, 'home.html', data)

def post(request,url):
    post=Post.objects.get(url=url)
    cats = Category.objects.all()
    #print(post)
    return render(request,'posts.html', {'post':post,'cats':cats})

def category(request,url):
    cat=Category.objects.get(url=url)
    posts=Post.objects.filter(cat=cat)
    return render(request,"category.html",{'cat':cat,'posts':posts})

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})