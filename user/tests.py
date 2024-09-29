from django.test import TestCase

from django.urls import include, path, reverse

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .models import User
from .serializers import UserSerializers
import json
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class TestMethodGetEndPointUsers(TestCase, URLPatternsTestCase):
    urlpatterns = [
            path('descbem', include('descbem.urls')),
        ]
    
    def setUp(self):
        self.user = User.objects.create(name='John', email='john@gmail.com', username='john', password='12345678')

    def tearDown(self): 
        User.objects.all().delete()

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_get_users(self):
        url = reverse('users')
        token = self.get_token(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_post_users(self):
        url_users = reverse('users')
        data_users = {
            "id": 1,
            "name": "Henry",
            "email": "henry@gmail.com",
            "username": "henry22",
            "password": "1234567890000",
            "token": json.dumps(["dy2liFKToR5-5Tq_N2suen:APA91bGstv9_ljvnwX-XZ0OkJQFj29Dxb4Vgifom1qs2gG2Ev9OV1X5hxYXsoVwdy317hfFW_60S6XotIMHJNcimwIds", "-QFk6dS-cSqckjaXclq-wM9kGnXkxHPgolIghPxMqlXSgSvP"])
        }
        
        token = self.get_token(self.user)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json' 
        }
        response = self.client.post(url_users, data=json.dumps(data_users), content_type='application/json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['data']['email'], data_users['email'])

    def test_post_users_400_bad_request(self):
        url_users = reverse('users')
        data_users = {
            "name": "henry",
            "username": "henry22",
            "password": "123456789000",

        }

        token = self.get_token(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = self.client.post(url_users, data_users, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_under_min_length_required(self):
        url_users = reverse('users')
        data_users = {
            "name": "henry",
            "username": "henry22",
            "password": "12345678",
            "email": "teste@gmail.com"
        }
        
        response = self.client.post(url_users, data=data_users, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_user_without_password(self):
        url_users = reverse('users')
        data_users = {
            "name": "henry",
            "username": "henry22",
            "email": "teste@gmail.com"
        }
        
        response = self.client.post(url_users, data=data_users, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestMethodPutEndPointUser(APITestCase):

    def setUp(self):
        self.user = User.objects.create(name='John', email='john@gmail.com', username='john')
        self.user.set_password('12345678')
        self.user.save()

    def tearDown(self): 
        User.objects.all().delete()

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_put_users(self):
        url = reverse('users-detail', kwargs={'pk': self.user.id})
        data_users = {
            "name": "James",
            "email": "james@gmail.com",
            "username": "james",
            "password": "12345678"

        }

        token = self.get_token(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = self.client.put(url, data_users, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.user.refresh_from_db()
        self.assertEqual(response.data, {'message': 'Usuário atualizado com sucesso.'})

    def test_put_users_error_404_not_found(self):
        url = reverse('users-detail', kwargs={'pk': 10000})
        data_users = {
            "name": "James",
            "email": "james@gmail.com",
            "username": "james",
            "password": "12345678"

        }

        token = self.get_token(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = self.client.put(url, data_users, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_put_error_401_unauthorized(self):
        url = reverse('users-detail', kwargs={'pk': self.user.id})
        data_users = {
            "name": "James",
            "email": "james@gmail.com",
            "username": "james",
            "password": "12345678"

        }

        response = self.client.put(url, data_users, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password(self): 
        url = reverse('auth-change-password', kwargs={'pk': self.user.id})
        change_password_data = {
            "old_password":'12345678',
            "password": "87654321",
            "password2": "87654321"
        }

        token = self.get_token(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = self.client.put(url, change_password_data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.password, self.user.check_password('87654321'))
        
    def test_delete_users(self):
        token = self.get_token(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        url = reverse('users-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.filter(id=self.user.pk).get().is_active, False) 
    
    def test_filter_by_email_user(self):
        token = self.get_token(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        url = reverse('user-search')

        response = self.client.get(url, {'email': 'john@gmail.com'}, **headers)
        user = User.objects.filter(email='john@gmail.com')
        serializer = UserSerializers(user, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data) 
        self.assertEqual(len(response.data), 1)


    def test_password_reset_request(self):
        url = reverse('password-reset-request')
        data = {'email': 'john@gmail.com'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password Reset')
        self.assertEqual(mail.outbox[0].to, ['john@gmail.com'])
        self.assertIn('Clique no link a seguir para redefinir sua senha:', mail.outbox[0].body)
        

class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name='John', email='john@gmail.com', username='john')
        self.user.set_password('12345678')
        self.user.save()

    def test_password_reset_success(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        new_password = 'newpassword'

        url = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        data = {'password': new_password, 'password2': new_password, 'token': token}

        response = self.client.put(url, data=json.dumps(data), content_type='application/json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Redefinição de senha com sucesso'})
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_password_reset_invalid_token(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = 'invalidtoken'
        new_password = 'newpassword'

        url = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        data = {'password': new_password}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Token inválido'})
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(new_password))

    def test_password_reset_invalid_uid(self):
        uidb64 = urlsafe_base64_encode(force_bytes(9999))
        token = default_token_generator.make_token(self.user)
        new_password = 'newpassword'

        url = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        data = {'password': new_password}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Token inválido'})
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(new_password))