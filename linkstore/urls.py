from django.urls import path,include
from . import views

urlpatterns = [
    path('link1', views.link_page, name='homepage'),
    path('recent_link', views.recent_link, name='recent_link'),
    path('add_link', views.add_link, name='add_link'),
    path('form_edit/<int:pk>/', views.form_edit, name='form_edit'),
    path('delete_link/<int:pk>/', views.delete_link, name='delete_link'),
    path('view_links/<str:category>/', views.category_link, name='category_link'),
]