from django.urls import path
from blog.views import(
	create_post_view,
	detail_blog_view,
	add_to_projectlist
)

app_name = 'blog'

urlpatterns = [
	path('create', create_post_view, name="create"),
	path('<slug>/', detail_blog_view, name="detail"),
	path('add-to-projectlist/<slug>/', add_to_projectlist, name='add-to-projectlist'),
]