from django.urls import path
from blog.views import(
	create_post_view,
	detail_blog_view,
)

app_name = 'blog'

urlpatterns = [
	path('create', create_post_view, name="create"),
	path('<slug>/', detail_blog_view, name="detail")
]