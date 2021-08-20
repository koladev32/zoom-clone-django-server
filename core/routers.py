from rest_framework.routers import SimpleRouter
from core.user.viewsets import UserViewSet
from core.authentication.viewsets import LoginViewSet, RegistrationViewSet, RefreshViewSet
from core.room.viewsets import RoomViewSet

routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# USER
routes.register(r'user', UserViewSet, basename='user')

# ROOM
routes.register(r'room', RoomViewSet, basename='room')



urlpatterns = [
    *routes.urls
]