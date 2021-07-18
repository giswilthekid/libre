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
    service_view,
    profile_view,
    delete_language,
    delete_skill,
    delete_education,
)

from blog.views import(
    buyerpage
)

urlpatterns = [
    path('blog/', include('blog.urls', 'blog')),
    path('service/', include('service.urls', 'service')),
    path('', landing_view, name='landing'),
    path('admin/', admin.site.urls),
    path('buyerpage/', buyerpage, name='buyerpage'),
    path('projectlist/', project_view, name='projectlist'),
    path('servicelist/', service_view, name='servicelist'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('profile/<slug>/', profile_view, name='profile'),
    path('language/delete/<id>/', delete_language, name='delete-language'),
    path('skill/delete/<id>/', delete_skill, name='delete-skill'),
    path('education/delete/<id>/', delete_education, name='delete-education'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
