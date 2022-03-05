from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from base.models import User, Roles


class TestUserAPI(TestCase):
    seller_data = {'username': 'seller', 'password': 'password'}
    buyer_data = {'username': 'buyer', 'password': 'password'}

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'user',
            'password': 'password',
            'role': Roles.SELLER
        }
        self.seller = User.objects.create(
            username=self.seller_data['username'], role=Roles.SELLER)
        self.seller.set_password(self.seller_data['password'])
        self.seller.save()
        self.buyer = User.objects.create(
            username=self.buyer_data['username'], role=Roles.BUYER)
        self.buyer.set_password(self.buyer_data['password'])
        self.buyer.save()

    def set_client_credentials(self, auth_data):
        response = self.client.post(reverse('login'), auth_data)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access']
        )

    def test_anonymous_user_cannot_create_user(self):
        response = self.client.post(
            reverse('base:users-list'), self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(
            username=self.user_data['username']).exists())

    def test_anonymous_user_cannot_create_user_without_username(self):
        self.user_data.pop('username')
        response = self.client.post(
            reverse('base:users-list'), self.user_data)
        self.assertEqual(response.status_code, 400)

    def test_anonymous_user_cannot_edit_user(self):
        response = self.client.patch(
            reverse('base:users-detail',
                    args=[self.seller.id]),
            self.user_data)
        self.assertEqual(response.status_code, 401)

    def test_different_user_cannot_edit_not_his_data(self):
        self.set_client_credentials(self.seller_data)
        response = self.client.patch(
            reverse('base:users-detail', args=[self.buyer.id]), self.user_data)
        self.assertEqual(response.status_code, 404)

    def test_user_can_edit_his_data(self):
        self.set_client_credentials(self.seller_data)
        response = self.client.patch(
            reverse('base:users-detail', args=[self.seller.id]),
            {'role': Roles.BUYER})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['role'], Roles.BUYER)

    def test_anonymous_user_cannot_get_users_data(self):
        response = self.client.get(reverse('base:users-list'))
        self.assertEqual(response.status_code, 401)

    def test_user_cannot_get_all_users_data(self):
        self.set_client_credentials(self.buyer_data)
        response = self.client.get(reverse('base:users-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['users']), 1)

    def test_user_can_get_his_data(self):
        self.set_client_credentials(self.seller_data)
        response = self.client.get(
            reverse('base:users-detail', args=[self.seller.id]))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_get_another_user_data(self):
        self.set_client_credentials(self.seller_data)
        response = self.client.get(
            reverse('base:users-detail', args=[self.buyer.id]))
        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_his_data(self):
        self.set_client_credentials(self.seller_data)
        response = self.client.delete(
            reverse('base:users-detail', args=[self.seller.id]))
        self.assertEqual(response.status_code, 204)

    def test_user_cannot_delete_another_user_data(self):
        self.set_client_credentials(self.seller_data)
        response = self.client.delete(
            reverse('base:users-detail', args=[self.buyer.id]))
        self.assertEqual(response.status_code, 404)
