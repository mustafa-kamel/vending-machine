from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from base.models import User, Product, Roles


class TestProductAPI(TestCase):
    seller1_data = {'username': 'seller1', 'password': 'password'}
    seller2_data = {'username': 'seller2', 'password': 'password'}
    buyer_data = {'username': 'buyer', 'password': 'password'}

    def setUp(self):
        self.client = APIClient()
        self.seller1 = User.objects.create(
            username=self.seller1_data['username'], role=Roles.SELLER)
        self.seller1.set_password(self.seller1_data['password'])
        self.seller1.save()
        self.seller2 = User.objects.create(
            username=self.seller2_data['username'], role=Roles.SELLER)
        self.seller2.set_password(self.seller2_data['password'])
        self.seller2.save()
        self.buyer = User.objects.create(
            username=self.buyer_data['username'], role=Roles.BUYER)
        self.buyer.set_password(self.buyer_data['password'])
        self.buyer.save()
        self.product1 = Product.objects.create(
            name='Juice', price=10, available=12, seller=self.seller1)
        self.product2 = Product.objects.create(
            name='Coffee', price=15, available=9, seller=self.seller2)
        self.product_data = {
            'name': 'Water 600ml',
            'price': 5,
            'available': 3
        }

    def set_client_credentials(self, auth_data):
        response = self.client.post(reverse('login'), auth_data)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access']
        )

    def test_anonymous_user_cannot_create_product(self):
        response = self.client.post(
            reverse('base:products-list'), self.product_data)
        self.assertEqual(response.status_code, 401)

    def test_buyer_cannot_create_product(self):
        self.set_client_credentials(self.buyer_data)
        response = self.client.post(
            reverse('base:products-list'), self.product_data)
        self.assertEqual(response.status_code, 403)

    def test_seller_cannot_create_product_without_name(self):
        self.set_client_credentials(self.seller1_data)
        self.product_data.pop('name')
        response = self.client.post(
            reverse('base:products-list'), self.product_data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('name' in response.data)

    def test_seller_can_create_product(self):
        self.set_client_credentials(self.seller1_data)
        response = self.client.post(
            reverse('base:products-list'), self.product_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data['product']['name'], self.product_data['name'])

    def test_anonymous_user_cannot_edit_product(self):
        response = self.client.patch(
            reverse('base:products-detail',
                    args=[self.seller1.id]),
            self.product_data)
        self.assertEqual(response.status_code, 401)

    def test_different_seller_cannot_edit_product(self):
        self.set_client_credentials(self.seller1_data)
        response = self.client.patch(
            reverse('base:products-detail', args=[self.product2.id]),
            {'price': 5, 'available': 6})
        self.assertEqual(response.status_code, 403)

    def test_buyer_cannot_edit_product(self):
        self.set_client_credentials(self.buyer_data)
        response = self.client.patch(
            reverse('base:products-detail', args=[self.product2.id]),
            {'price': 5, 'available': 6})
        self.assertEqual(response.status_code, 403)

    def test_seller_can_edit_his_product(self):
        self.set_client_credentials(self.seller1_data)
        response = self.client.patch(
            reverse('base:products-detail', args=[self.product1.id]),
            {'price': 5, 'available': 6})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['product']['price'], 5)
        self.assertEqual(response.data['product']['available'], 6)

    def test_anonymous_user_can_get_all_products_data(self):
        response = self.client.get(reverse('base:products-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['products']), 2)

    def test_seller_can_get_all_products_data(self):
        self.set_client_credentials(self.seller1_data)
        response = self.client.get(reverse('base:products-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['products']), 2)

    def test_buyer_can_get_all_products_data(self):
        self.set_client_credentials(self.buyer_data)
        response = self.client.get(reverse('base:products-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['products']), 2)

    def test_seller_can_get_single_product_data(self):
        self.set_client_credentials(self.seller1_data)
        response = self.client.get(
            reverse('base:products-detail', args=[self.product2.id]))
        self.assertEqual(response.status_code, 200)

    def test_buyer_can_get_single_product_data(self):
        self.set_client_credentials(self.buyer_data)
        response = self.client.get(
            reverse('base:products-detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)

    def test_seller_can_delete_his_product(self):
        self.set_client_credentials(self.seller1_data)
        response = self.client.delete(
            reverse('base:products-detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, 204)

    def test_seller_cannot_delete_not_his_product(self):
        self.set_client_credentials(self.seller1_data)
        response = self.client.delete(
            reverse('base:products-detail', args=[self.product2.id]))
        self.assertEqual(response.status_code, 403)

    def test_buyer_cannot_delete_product(self):
        self.set_client_credentials(self.buyer_data)
        response = self.client.delete(
            reverse('base:products-detail', args=[self.product2.id]))
        self.assertEqual(response.status_code, 403)
