from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from account.views import(
    landing_view,
    registration_view,
    login_view,
    logout_view,
    project_view,
    profile_view,
)

from blog.views import(
    buyerpage
)

urlpatterns = [
    path('', landing_view, name='landing'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', 'blog')),
    path('buyerpage/', buyerpage, name='buyerpage'),
    path('projectlist/', project_view, name='projectlist'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('profile/', profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
