from django.urls import path

from . import views
app_name="post_apps"
#/post/...
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('index/', views.index_page, name='index_page'),
    path('create/',views.create_page,name="create"),

    path('<slug:slug>/detail/', views.detail_page, name='detail'),
    path('<slug:slug>/update/', views.update_page, name='update'),
    path('<slug:slug>/delete/', views.delete_page, name='delete'),
    #path('create/', views.home_page, name='home_page'),
    #path('update', views.home_page, name='home_page'),
    #path('delete', views.home_page, name='home_page'),
    #
]