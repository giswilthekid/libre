from django.urls import path
from blog.views import(
	create_post_view,
	detail_blog_view,
	add_to_projectlist,
	edit_post_view,
	delete_post_view,
	cancelled_project,
	load_subcategory,
)

app_name = 'blog'

urlpatterns = [
	path('create', create_post_view, name="create"),
	path('<slug>/', detail_blog_view, name="detail"),
	path('<slug>/edit/', edit_post_view, name="edit"),
	path('<slug>/delete/', delete_post_view, name="delete"),
	path('add-to-projectlist/<slug>/', add_to_projectlist, name='add-to-projectlist'),
	path('cancelled-project/<slug>/', cancelled_project, name='cancelled-project'),
	path('ajax/load-subcategory/', load_subcategory, name='ajax_load_subcategory'),
]