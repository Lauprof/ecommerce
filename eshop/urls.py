from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('products/',views.products, name='product'),
    path('login/',views.login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('reset/',views.reset_password,name='reset'),
    path("register/", views.register, name="register"),
    path('addproduct/',views.add_products, name='addproduct'),
    path('edit/<int:id>/', views.edit_product, name='editproduct'),
    path('delete/<int:id>',views.delete_product,name='deleteproduct')
    
]