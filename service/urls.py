from django.urls import path

from service.views import(
	sellerpage,
	create_service_view,
	detail_service_view,
	add_to_servicelist,
	cancelled_service,
	edit_service_view,
	delete_service_view
)

app_name = 'service'

urlpatterns = [
	path('sellerpage/', sellerpage, name="sellerpage"),
	path('create-service/', create_service_view, name="create-service"),
	path('<slug>/', detail_service_view, name="detail-service"),
	path('add-to-servicelist/<slug>/<packet_id>/<tipe_packet>', add_to_servicelist, name='add-to-servicelist'),
	path('cancelled-service/<slug>/', cancelled_service, name='cancelled-service'),
	path('<slug>/edit/', edit_service_view, name="edit"),
	path('<slug>/delete/', delete_service_view, name="delete"),
]