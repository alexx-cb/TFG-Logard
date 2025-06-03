from django.conf.urls.static import static
from django.urls import path


from LogardBackEnd import settings


from .views.apiView import APIRootView
from .views.categoryView import CategoryListCreateView, CategoryDetailsView, CategoryByNameView
from .views.productView import ProductListCreateView, ProductDetailsView, ProductByNameView, ProductListCategoryView
from .views.tokenView import CustomTokenObtainPairView, CookieTokenRefreshView, CookieLogoutView
from .views.userView import UserRegisterView, CurrentUserView, VerifyUserView

urlpatterns = [

    path('', APIRootView.as_view(), name='api-root'),

    # Usuario
    path('user/', UserRegisterView.as_view(), name='user-register'),
    path('me/', CurrentUserView.as_view(), name='user-detail'),


    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailsView.as_view(), name='category-detail'),
    path('categories/search/<str:name>/', CategoryByNameView.as_view(), name='category-search'),

    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/category/<int:pk>/', ProductListCategoryView.as_view(), name='product-category'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),
    path('products/search/<str:name>/', ProductByNameView.as_view(), name='product-search'),

    # JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh-cookie/', CookieTokenRefreshView.as_view(), name='token_refresh_cookie'),
    path('cookie-logout/', CookieLogoutView.as_view(), name='cookie_logout'),
    path('verify/', VerifyUserView.as_view(), name='verify-user'),

]