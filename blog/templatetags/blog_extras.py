import logging
from django.contrib.auth import get_user_model
from django.template import Library
from django.utils.html import format_html

from blog.models import Post

logger = logging.getLogger(__name__)

user = get_user_model()

register = Library()

@register.filter
def author_details(author, current_user=None):
  if not isinstance(author, user):
    return ""

  if author == current_user:
    return format_html("<strong>Me</strong>")

  if author.first_name and author.last_name:
    name = f"{author.first_name} {author.last_name}"
  else:
    name = f"{author.username}"

  if author.email:
    prefix = format_html('<a href="mailto:{}">', author.email)
    suffix = format_html("</a>")
  else:
    prefix = ""
    suffix = ""
  
  return format_html("{}{}{}", prefix, name, suffix)

@register.simple_tag(name="row")
def bootstrap_row(extra_classes=""):
  return format_html('<div class="row {} ">', extra_classes)

@register.simple_tag(name="endrow")
def bootstrap_endrow():
  return format_html('</div>')

@register.simple_tag(name="col")
def bootstrap_row(extra_classes=""):
  return format_html('<div class="col {} ">', extra_classes)

@register.simple_tag(name="endcol")
def bootstrap_endrow():
  return format_html('</div>')

@register.inclusion_tag("blog/post_list.html")
def recent_posts(post):
  posts = Post.objects.exclude(pk=post.pk)[:5]
  logger.debug("Loaded %d recent posts for post %d", len(posts), post.pk)
  context = {
    "title": "Recent Posts", 
    "posts": posts
  }
  return context
