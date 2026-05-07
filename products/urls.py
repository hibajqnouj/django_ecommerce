from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<int:id>/", views.product_detail, name="product_detail"),
    path("categories/", views.category_list, name="category_list"),
    path("category/<int:id>/", views.category_detail, name="category_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
]
