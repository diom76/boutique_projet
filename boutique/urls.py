from django.urls import path
from .import views

app_name ='boutique'

urlpatterns = [
    path('',views.liste_produits, name='liste'),
    path('<int:pk>/', views.detail_produit, name='detail'),
    path('confirmation/<int:pk>/',views.confirmation, name='confirmation'),
    path('contact/',views.contact, name='contact'),
    path('inscription/',views.inscription, name='inscription'),
    path('profil/',views.profil, name='profil'),
    path('admin-dashboard/',views.admin_dashboard, name='admin_dashboard')
]
