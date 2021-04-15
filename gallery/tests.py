import os

from django.conf import settings
from django.test import TestCase, Client, RequestFactory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status

from gallery import models
from gallery.api import serializers
from account.models import MyUser


client = Client()


class ModelsTest(TestCase):

    def setUp(self):
        user_misha = MyUser.objects.create_user(username='Misha',
                                                email='misha@test.com',
                                                password='banan007')
        user_kolya = MyUser.objects.create_user(username='Kolya',
                                                email='kolya@test.com',
                                                password='banan008')

        album_museum = models.Album.objects.create(owner=user_misha, name="Museum")
        album_dacha = models.Album.objects.create(owner=user_misha, name="Dacha")

        image_path = os.path.join(settings.MEDIA_ROOT, 'test_image.jpg')
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpg')

        photo_museum = models.Photo.objects.create(owner=user_misha, album=album_museum, photo=image)
        photo_dacha = models.Photo.objects.create(owner=user_misha, album=album_dacha, photo=image,
                                                  description="I'm at the dacha")

        comment_museum_1 = models.Comment.objects.create(owner=user_kolya, photo=photo_museum, text="You look smart")
        comment_museum_2 = models.Comment.objects.create(owner=user_misha, photo=photo_museum, text="Only look?")
        comment_dacha = models.Comment.objects.create(owner=user_misha, photo=photo_dacha, text="Kebabs with friends")

        bookmark_museum = models.Bookmark.objects.create(owner=user_kolya, photo=photo_museum)

        comment_museum_2.delete()

    def test_users(self):
        user_misha = MyUser.objects.get(username='Misha')
        user_kolya = MyUser.objects.get(email='kolya@test.com')

        self.assertEquals(user_misha.email, 'misha@test.com')
        self.assertNotEquals(user_kolya.username, 'Dima')
        self.assertNotEquals(user_kolya.password, 'banan008')

    def test_albums(self):
        album_museum = models.Album.objects.get(name="Museum")
        album_dacha = models.Album.objects.get(name="Dacha")

        self.assertEquals(album_museum.name, 'Museum')
        self.assertNotEquals(album_dacha.name, 'Forest')
        self.assertNotEquals(album_dacha.owner.email, 'vova@test.com')

    def test_photos(self):
        photo_museum = models.Photo.objects.get(album__name="Museum")
        photo_dacha = models.Photo.objects.get(album__name="Dacha")

        self.assertEquals(photo_museum.description, '')
        self.assertNotEquals(photo_museum.description, "I'm at the dacha")
        self.assertNotEquals(photo_dacha.album.name, 'Pool')

    def test_comments(self):
        comments_museum = models.Comment.objects.filter(photo__album__name='Museum')
        comment_dacha = models.Comment.objects.get(photo__album__name='Dacha')

        self.assertEquals(comment_dacha.text, 'Kebabs with friends')
        self.assertNotEquals(len(comments_museum), 2)

    def test_bookmarks(self):
        bookmark_museum = models.Bookmark.objects.get(photo__album__name='Museum')

        self.assertEquals(bookmark_museum.photo.description, '')
        self.assertNotEquals(bookmark_museum.owner.username, 'Misha')


class SerializersTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        request = self.request_factory.get('/')

        user_misha = MyUser.objects.create_user(username='Misha',
                                                email='misha@test.com',
                                                password='banan007')

        self.album_attributes = {
            'owner': user_misha,
            'name': 'Holidays'
        }
        self.album_serializer_data = {
            'name': 'Holidays'
        }
        self.album = models.Album.objects.create(**self.album_attributes)
        self.album_serializer = serializers.AlbumSerializerWrite(instance=self.album)

        image_path = os.path.join(settings.MEDIA_ROOT, 'test_image.jpg')
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpg')

        self.photo_attributes = {
            'owner': user_misha,
            'album': self.album,
            'photo': image,
            'description': 'Me with my family'
        }

        self.photo_serializer_data = {
            'description': 'Me with my family'
        }
        self.photo = models.Photo.objects.create(**self.photo_attributes)
        self.photo_serializer = serializers.PhotoSerializerWrite(instance=self.photo)

        self.comment_attributes = {
            'owner': user_misha,
            'photo': self.photo,
            'text': 'Hi there!'
        }
        self.comment_serializer_data = {
            'text': 'Hi there!'
        }
        self.comment = models.Comment.objects.create(**self.comment_attributes)
        self.comment_serializer = serializers.CommentSerializerWrite(instance=self.comment)

    def test_albums(self):
        data = self.album_serializer.data
        self.assertEqual(data['name'], self.album_serializer_data['name'])

    def test_photos(self):
        data = self.photo_serializer.data
        self.assertEqual(data['description'], self.photo_serializer_data['description'])

    def test_comments(self):
        data = self.comment_serializer.data
        self.assertEqual(data['text'], self.comment_serializer_data['text'])

    def test_bookmarks(self):
        pass


class RoutesAndViewsTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

        user_misha = MyUser.objects.create_user(username='Misha',
                                                email='misha@test.com',
                                                password='banan007')
        user_kolya = MyUser.objects.create_user(username='Kolya',
                                                email='kolya@test.com',
                                                password='banan008')

        album_museum = models.Album.objects.create(owner=user_misha, name="Museum")
        album_dacha = models.Album.objects.create(owner=user_misha, name="Dacha")

        image_path = os.path.join(settings.MEDIA_ROOT, 'test_image.jpg')
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                   content_type='image/jpg')

        photo_museum = models.Photo.objects.create(owner=user_misha, album=album_museum, photo=image)
        photo_dacha = models.Photo.objects.create(owner=user_misha, album=album_dacha, photo=image,
                                                  description="I'm at the dacha")

        comment_museum_1 = models.Comment.objects.create(owner=user_kolya, photo=photo_museum, text="You look smart")
        comment_museum_2 = models.Comment.objects.create(owner=user_misha, photo=photo_museum, text="Only look?")
        comment_dacha = models.Comment.objects.create(owner=user_misha, photo=photo_dacha, text="Kebabs with friends")

        bookmark_museum = models.Bookmark.objects.create(owner=user_kolya, photo=photo_museum)

        comment_museum_2.delete()

    def test_albums(self):

        response = client.get(reverse('gallery_api:album-list'))

        albums = models.Album.objects.all()

        request = self.request_factory.get(reverse('gallery_api:album-list'))
        serializer = serializers.AlbumSerializerRead(albums, many=True, context={'request': request})

        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_photos(self):

        response = client.get(reverse('gallery_api:photo-list'))

        photos = models.Photo.objects.all()

        request = self.request_factory.get(reverse('gallery_api:photo-list'))
        serializer = serializers.PhotoSerializerRead(photos, many=True, context={'request': request})

        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comments(self):

        response = client.get(reverse('gallery_api:comment-list'))

        comments = models.Comment.objects.all()

        request = self.request_factory.get(reverse('gallery_api:comment-list'))
        serializer = serializers.CommentSerializerRead(comments, many=True, context={'request': request})

        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bookmarks(self):

        response = client.get(reverse('gallery_api:bookmark-list'))

        bookmarks = models.Bookmark.objects.all()

        request = self.request_factory.get(reverse('gallery_api:bookmark-list'))
        serializer = serializers.BookmarkSerializerRead(bookmarks, many=True, context={'request': request})

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)


