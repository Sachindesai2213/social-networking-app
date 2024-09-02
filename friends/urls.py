from rest_framework import routers
from .views import FriendViewSet, FriendRequestViewSet


router = routers.DefaultRouter()
router.register('friends', FriendViewSet)
router.register('friend-requests', FriendRequestViewSet)

urlpatterns = []

urlpatterns += router.urls
