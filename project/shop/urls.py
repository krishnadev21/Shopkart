from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('register/', views.register, name='register'),
    path('collections/', views.collection, name='collections'),
    path('collections/<str:name>', views.collectionView, name='collections'),
    path('product-details/<str:cname>/<str:pname>/', views.productDetails, name='product-details'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.addToCart, name='add-to-cart'),
    path('remove-cart/<str:pk>', views.removeCart, name='remove-cart'),
    path('favourities/', views.favourities, name='favourities'),
    path('add-to-fav/', views.addToFav, name='add-to-fav'),
    path('remove-fav/<str:pk>', views.removeFavourite, name='remove-fav'),
]