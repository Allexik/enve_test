from django.urls import include, path
from rest_framework import routers
from gallery.api import views


router = routers.DefaultRouter()
router.register(r'albums', views.AlbumViewSet)
router.register(r'photos', views.PhotoViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'bookmarks', views.BookmarkViewSet)

router.register(r'feed', views.FeedViewSet, basename='feed')

urlpatterns = [
    path('', include(router.urls))
]

