from . import views
from django.urls import path

urlpatterns = [
    path('books/', views.book_list, name='book-list'),
    path('books/new/', views.Create_book, name='create-book'), 
    path('books/<int:book_id>/', views.book_detail, name='book-detail'),
    path('books/<int:book_id>/update/', views.update_book, name='update-book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete-book'),

    path('categorys/', views.category_list, name='category-list'),
    path('categorys/new/', views.create_category, name='create-category'), 
    path('categorys/<int:book_id>/', views.category_detail, name='category-detail'),
    path('categorys/<int:book_id>/update/', views.update_category, name='update-category'),
    path('categorys/<int:book_id>/delete/', views.delete_category, name='delete-category'),

    path('orders/', views.order_list, name='order-list'),
    path('orders/new/', views.create_order, name='create-order'), 
    path('orders/<int:order_id>/', views.order_detail, name='order-detail'),
    path('orders/<int:order_id>/update/', views.update_order, name='update-order'),
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete-order'),

    
]