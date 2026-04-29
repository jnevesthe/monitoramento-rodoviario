from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views 
from .views import List, Create, Edit, Detail, Delete

urlpatterns=[

    path('users/', List.as_view(), name='user'),
    path('create/', Create.as_view(), name='create'),
    path('delet/<int:pk>/', Delete.as_view(), name='delet'),
    path('detail/<int:pk>/', Detail.as_view(), name='detail'),
    path('edit/<int:pk>/', Edit.as_view(), name='edit'),
    path('word/<int:pk>/', views.word, name='word'),
    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
