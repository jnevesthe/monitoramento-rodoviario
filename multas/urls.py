from django.urls import path, re_path
from . import views
from .views import List,Detail,Delete

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('api/multar/', views.api_multar, name='api_multar'),
    path('list/', List.as_view(), name='list'),
    path('listb/', views.listb, name='listb'),
    path('logout_confirm/', views.logout_confirm, name='logout_confirm'),
    path('list/<int:pk>/', Detail.as_view(), name='lista'),
    path('get/', views.get_view, name='get'),
    path('multar/<int:pk>/', views.multar, name='multar'),  
    path('confirm/<int:pk>/', views.confirm, name='confirm'), 
    path('delete/<int:pk>/', Delete.as_view(), name='delete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),    
    path('confirmar_multa/<int:pk>/', views.confirmar_multa, name='confirmar_multa'),
    re_path(r'^.*$/', views.pagina_404),

    #path('detail/<int:pk>/', Detail.as_view(), name='detail_veiculo'),  # 👈 ESTE ESTAVA FALTANDO

    #path('api/multar/', api_multar, name='api_multar'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



#Josemar Neves

































#Josemar Neves
