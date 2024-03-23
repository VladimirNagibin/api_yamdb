from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminUserViewSet, UserCreateViewSet, UserTokenCreateViewSet

router_v1 = DefaultRouter()
router_v1.register('users', AdminUserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/',
         UserCreateViewSet.as_view({'post': 'create'}),
         name='registration'),
    path('v1/auth/token/',
         UserTokenCreateViewSet.as_view({'post': 'create'}),
         name='token'),
    path('v1/', include(router_v1.urls)),
]
