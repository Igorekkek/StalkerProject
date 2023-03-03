from django.contrib import admin
from django.urls import path
from ServerAPI.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/addNewData/', AddNewDataView.as_view()),
    path('api/getMapUrl/', GetMapUrlView.as_view()),
    path('api/deleteData/', DeleteAllDataView.as_view()),
    path('api/swans/', SwanListView.as_view()),
    path('api/detectors/', DetectorListView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
