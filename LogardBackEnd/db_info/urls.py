from django.conf.urls.static import static
from django.urls import path


from LogardBackEnd import settings
from .views.MergeCartView import MergeCartView

from .views.apiView import APIRootView
from .views.cartView import CartDetailView, UpdateCartItemView, ClearCartView
from .views.categoryView import CategoryListCreateView, CategoryDetailsView, CategoryByNameView
from .views.productView import ProductListCreateView, ProductDetailsView, ProductByNameView, ProductListCategoryView, \
    product_info_list
from .views.tokenView import CustomTokenObtainPairView, CookieTokenRefreshView, CookieLogoutView
from .views.userView import UserRegisterView, CurrentUserView, VerifyUserView

urlpatterns = [

    path('', APIRootView.as_view(), name='api-root'),

    # User
    path('user/', UserRegisterView.as_view(), name='user-register'),
    path('me/', CurrentUserView.as_view(), name='user-detail'),


    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailsView.as_view(), name='category-detail'),
    path('categories/search/<str:name>/', CategoryByNameView.as_view(), name='category-search'),

    # Products
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/category/<int:pk>/', ProductListCategoryView.as_view(), name='product-category'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),
    path('products/search/<str:name>/', ProductByNameView.as_view(), name='product-search'),
    path('products/info/', product_info_list, name='product-info'),

    #Cart
    path('cart/', CartDetailView.as_view(), name='cart-details'),
    path('cart/update/<int:pk>/', UpdateCartItemView.as_view(), name='cart-update'),
    path('cart/merge/', MergeCartView.as_view(), name='cart-merge'),
    path('cart/clear/', ClearCartView.as_view(), name='cart-clear'),

    # JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh-cookie/', CookieTokenRefreshView.as_view(), name='token_refresh_cookie'),
    path('cookie-logout/', CookieLogoutView.as_view(), name='cookie_logout'),
    path('verify/', VerifyUserView.as_view(), name='verify-user'),

]