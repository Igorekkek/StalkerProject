from django.contrib import admin
from django.urls import path
from ServerAPI.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/AddNewData/', AddNewDataView.as_view()),
]
