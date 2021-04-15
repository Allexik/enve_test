from django.core.exceptions import FieldError
from rest_framework import viewsets, generics, permissions, mixins, filters
from gallery.permissions import IsOwner
from gallery import models
from gallery.api import serializers
from utils.exceptions import FieldException
from utils.mixins import ReadWriteSerializerMixin

from django.db.models import Count

from django_filters.rest_framework import DjangoFilterBackend


class MainMixin(ReadWriteSerializerMixin):
    filterset_fields = ['owner']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AlbumViewSet(MainMixin, viewsets.ModelViewSet):
    queryset = models.Album.objects.all() \
        .order_by('name')
    read_serializer_class = serializers.AlbumSerializerRead
    write_serializer_class = serializers.AlbumSerializerWrite

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class PhotoViewSet(MainMixin, viewsets.ModelViewSet):
    queryset = models.Photo.objects.all() \
        .order_by('album__name')
    read_serializer_class = serializers.PhotoSerializerRead
    write_serializer_class = serializers.PhotoSerializerWrite

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http_method_names = list(filter(lambda x: x != 'put', self.http_method_names))  # exclude put

        self.filterset_fields = self.filterset_fields + ['album', 'album__name', 'description']

    def get_serializer_class(self):
        if self.action == "partial_update":
            return serializers.PhotoSerializerPatch
        elif self.action in ["create", "update", "destroy"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class CommentViewSet(MainMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = models.Comment.objects.all() \
        .order_by('photo__album__name')
    read_serializer_class = serializers.CommentSerializerRead
    write_serializer_class = serializers.CommentSerializerWrite

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filterset_fields = self.filterset_fields + ['photo', 'photo__description', 'text']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class BookmarkViewSet(MainMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsOwner]
    queryset = models.Bookmark.objects.all() \
        .order_by('photo__album__name')
    read_serializer_class = serializers.BookmarkSerializerRead
    write_serializer_class = serializers.BookmarkSerializerWrite

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filterset_fields = self.filterset_fields + ['photo', 'photo__description']

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(owner=self.request.user)

        return queryset


class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = models.Photo.objects.all() \
        .annotate(comments_count=Count('comment')) \
        .order_by('-comments_count')
    serializer_class = serializers.PhotoSerializerRead
