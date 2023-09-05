from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('menu-items/', views.menu_items),
    path('menu-items/<int:pk>', views.singlemenu_items),
    path('category/<int:pk>', views.category_detail, name='category-detail'),
    path('get-token', obtain_auth_token),
    path('manager-view', views.manager_view),
    path('path-throttle', views.throttle_check),
    path('path-throttle-auth', views.throttle_check_auth),
    path('groups/manager/users/<int:pk>', views.managers),
    path('groups/delivery-crew/users/<int:pk>', views.delivery_crew),
    path('menuoftheday', views.menu_feature),
    path('menuoftheday/<int:pk>', views.updated_menu_feature),
    path('cart/menu-items', views.listcart),
    path('orders', views.orders),
    path('orders/<int:pk>', views.single_order)
]
# class based views
""" 
    path('menu-items', views.MenuItemViews.as_view()),
    path('category', views.CategoryViews.as_view()),    
    path('menu-items/<int:pk>', views.SingleMenuItemViews.as_view()),
"""
