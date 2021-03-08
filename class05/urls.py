from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path, include

from class05 import settings
from manga import views

urlpatterns = [
    # views
    path('admin/', admin.site.urls),
    path('craw/', views.main_function),
    path('novels/', views.index),
    path('novels/<str:novel_name>', views.novel),
    path('novel/<str:chapter_title>', views.chapter_detail)

]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
