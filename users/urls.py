from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import SignupView, TestView, ForgetPasswordView, ResetPasswordView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', TestView.as_view(), name='test'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

]
