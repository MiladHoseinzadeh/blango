import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from blog.forms import CommentForm
from blog.models import Post, Comment

logger = logging.getLogger(__name__)

def index(request):
  posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")
  logger.debug("Got %d posts", len(posts))
  context = {
    "posts": posts,
  }
  return render(request, "blog/index.html", context)

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)

  if request.user.is_active:
    if request.method == "POST":
      comment_form = CommentForm(request.POST)

      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.content_object = post
        comment.creator = request.user
        comment.save()
        logger.info("Created comment on Post %d for user %s", post.pk, request.user)
        return redirect(request.path_info)

    else:
      comment_form = CommentForm()

  else:
    comment_form = None

  context = {
    "post": post,
    "comment_form": comment_form,
  }
  return render(request, "blog/post_detail.html", context)

def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])

# 192.168.11.179