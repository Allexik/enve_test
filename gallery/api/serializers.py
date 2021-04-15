from rest_framework import serializers

from account.api.serializers import MyUserSerializer
from gallery import models


class AlbumSerializerRead(serializers.HyperlinkedModelSerializer):
    owner = MyUserSerializer()

    class Meta:
        model = models.Album
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'gallery_api:album-detail'}
        }


class AlbumSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = models.Album
        exclude = ('owner',)


class PhotoSerializerRead(serializers.HyperlinkedModelSerializer):
    owner = MyUserSerializer()
    album = AlbumSerializerRead()

    class Meta:
        model = models.Photo
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'gallery_api:photo-detail'}
        }


class PhotoSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = models.Photo
        exclude = ('owner',)


class PhotoSerializerPatch(serializers.ModelSerializer):

    class Meta:
        model = models.Photo
        exclude = ('owner', 'photo')


class CommentSerializerRead(serializers.HyperlinkedModelSerializer):
    owner = MyUserSerializer()
    photo = PhotoSerializerRead()

    class Meta:
        model = models.Comment
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'gallery_api:comment-detail'}
        }


class CommentSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        exclude = ('owner',)


class BookmarkSerializerRead(serializers.HyperlinkedModelSerializer):
    owner = MyUserSerializer()
    photo = PhotoSerializerRead()

    class Meta:
        model = models.Bookmark
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'gallery_api:bookmark-detail'}
        }


class BookmarkSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = models.Bookmark
        exclude = ('owner',)

