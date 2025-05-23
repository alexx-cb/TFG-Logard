from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from LogardBackEnd import settings
from .views import VerifyUserView, UserRegisterView, CurrentUserView, APIRootView, CategoryByNameView, \
    CategoryDetailsView, CategoryListCreateView, ProductByNameView, ProductListCreateView, ProductDetailsView, \
    CookieLogoutView, CustomTokenObtainPairView, CookieTokenRefreshView

urlpatterns = [

    path('', APIRootView.as_view(), name='api-root'),

    # Usuario
    path('user/', UserRegisterView.as_view(), name='user-register'),
    path('me/', CurrentUserView.as_view(), name='user-detail'),


    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailsView.as_view(), name='category-detail'),
    path('categories/search/<str:name>', CategoryByNameView.as_view(), name='category-search'),

    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),
    path('products/search/<str:name>/', ProductByNameView.as_view(), name='product-search'),

    # JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh-cookie/', CookieTokenRefreshView.as_view(), name='token_refresh_cookie'),
    path('cookie-logout/', CookieLogoutView.as_view(), name='cookie_logout'),
    path('verify/', VerifyUserView.as_view(), name='verify-user'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)