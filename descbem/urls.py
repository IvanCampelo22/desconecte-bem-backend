from django.contrib import admin
from django.urls import path, re_path, include
from user import views as user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from notification import views as notification
from rest_framework import routers
from socialemotional import views as socialemotional

router = routers.DefaultRouter()
router.register(r'image', user.ImageUploadViewSet, basename='image')

urlpatterns = [
    path(r'api/', include(router.urls)),
    path('admin/', admin.site.urls),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('users/', user.UsersView.as_view(), name="users"),
    path('users/<int:pk>/', user.UsersDetailView.as_view(), name="users-detail"),
    re_path('user/search/$', user.UserList.as_view(), name='user-search'),
    path('change_password/<int:pk>/', user.ChangePasswordView.as_view(), name='auth-change-password'),
    path('password_reset/', user.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password_reset/<str:uidb64>/<str:token>/', user.PasswordResetView.as_view(), name='password-reset-confirm'),

    path('notifications/', notification.NotificationView.as_view(), name='notifications'),
    path('notifications/<int:pk>/', notification.NotificationDetailView.as_view(), name="notifications-detail"),

    path('socialmidiause/', socialemotional.SocialMidiaUseView.as_view(), name='socialmidiause'),
    path('socialmidiause/<int:pk>/', socialemotional.SocialMidiaUseDetailView.as_view(), name='socialmidiause'),
]