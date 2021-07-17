from django.urls import path

from service.views import(
	sellerpage,
	create_service_view,
)

app_name = 'service'

urlpatterns = [
	path('sellerpage/', sellerpage, name="sellerpage"),
	path('create-service/', create_service_view, name="create-service"),
]