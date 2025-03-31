# expenses/tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from expenses.models import Occasion, Event,Utlizers,Payment  # Adjust the import based on your actual models


User = get_user_model()

class BaseTestCase(APITestCase):

    def setUp(self):
        # Set up the test environment
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.user2 = User.objects.create_user(email='test1@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.occasion = Occasion.objects.create(name='Birthday Party', created_by=self.user)
        self.event = Event.objects.create(name='Cake Cutting', occasion=self.occasion, total_amount=100, expender=self.user, created_by=self.user)
        self.utilizer = Utlizers.objects.create(event=self.event, utlizer=self.user, amount=50)
        self.utilizer = Utlizers.objects.create(event=self.event, utlizer=self.user2, amount=50)
        self.payment = Payment.objects.create(payer=self.user2, payee=self.user, event=self.event, amount=10)


class OccasionManagementViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()  # Call the setup method of the base class
        self.list_url = reverse('occassion-list')

    def test_list_occasions(self):
        # Test listing occasions
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_occasion(self):
        # Test creating an occasion
        data = {'name': 'Wedding'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Wedding')

    def test_update_occasion(self):
        # Test updating an occasion
        url = reverse('occassion-detail', args=[self.occasion.id])
        data = {'name': 'Updated Birthday Party'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Birthday Party')

    def test_delete_occasion(self):
        # Test deleting an occasion
        url = reverse('occassion-detail', args=[self.occasion.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Occasion.objects.filter(id=self.occasion.id).exists())

    def test_occasion_summary(self):
        # Test retrieving the summary of an occasion
        url = reverse('occassion-summary', args=[self.occasion.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_expenditure'], 100)
        self.assertEqual(len(response.data['events']), 1)

    # Failure Test Cases
    def test_create_occasion_with_missing_data(self):
        # Test creating an occasion with missing data
        data = {}  # Missing required 'name' field
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_occasion_with_invalid_data(self):
        # Test creating an occasion with invalid data
        data = {'name': ''}  # Invalid 'name' field (empty string)
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_occasion_with_invalid_data(self):
        # Test updating an occasion with invalid data
        url = reverse('occassion-detail', args=[self.occasion.id])
        data = {'name': ''}  # Invalid 'name' field (empty string)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_nonexistent_occasion(self):
        # Test deleting a non-existent occasion
        url = reverse('occassion-detail', args=[999])  # Non-existent occasion ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_occasion_summary_nonexistent_occasion(self):
        # Test retrieving the summary of a non-existent occasion
        url = reverse('occassion-summary', args=[999])  # Non-existent occasion ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_list_occasions_unauthenticated(self):
        # Test listing occasions without authentication
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_occasion_unauthenticated(self):
        # Test creating an occasion without authentication
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        data = {'name': 'Wedding'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_occasion_unauthenticated(self):
        # Test updating an occasion without authentication
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = reverse('occassion-detail', args=[self.occasion.id])
        data = {'name': 'Updated Birthday Party'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_occasion_unauthenticated(self):
        # Test deleting an occasion without authentication
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = reverse('occassion-detail', args=[self.occasion.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_occasion_summary_unauthenticated(self):
        # Test retrieving the summary of an occasion without authentication
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = reverse('occassion-summary', args=[self.occasion.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class EventViewSetTests(BaseTestCase):
  
    def test_list_events(self):
        # Test listing events
        list_url = reverse('events-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_event(self):
        # Test creating an event
        list_url = reverse('events-list')
        data = {
            'name': 'Dinner Party',
            'occasion': self.occasion.id,
            'expender': self.user.id,
            'total_amount': 200,
            'utilizers_data': [{'utlizer': self.user.id, 'amount': 100}]
        }
        response = self.client.post(list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Dinner Party')

    def test_retrieve_event(self):
        # Test retrieving an event
        url = reverse('events-detail', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Cake Cutting')

    def test_update_event(self):
        # Test updating an event
        url = reverse('events-detail', args=[self.event.id])
        data = {
            'name': 'Updated Cake Cutting',
            'occasion': self.occasion.id,
            'expender': self.user.id,
            'total_amount': 150,
            'utilizers_data': [{'utlizer': self.user.id, 'amount': 75}]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Updated Cake Cutting')

    def test_delete_event(self):
        # Test deleting an event
        url = reverse('events-detail', args=[self.event.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_event_payments(self):
        # Test retrieving payments for an event
        url = reverse('events-payments', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # # Failure Test Cases
    def test_create_event_with_invalid_data(self):
        # Test creating an event with invalid data
        list_url = reverse('events-list')
        data = {
            'name': '',
            'occasion': self.occasion.id,
            'expender': self.user.id,
            'total_amount': 200,
            'utilizers_data': [{'utlizer': self.user.id, 'amount': 300}]  # Amount exceeds total_amount
        }
        response = self.client.post(list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_event(self):
        # Test retrieving a non-existent event
        url = reverse('events-detail', args=[999])  # Non-existent event ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_event_with_invalid_data(self):
        # Test updating an event with invalid data
        url = reverse('events-detail', args=[self.event.id])
        data = {
            'name': '',
            'occasion': self.occasion.id,
            'expender': self.user.id,
            'total_amount': 150,
            'utilizers_data': [{'utlizer': self.user.id, 'amount': 200}]  # Amount exceeds total_amount
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_nonexistent_event(self):
        # Test deleting a non-existent event
        url = reverse('events-detail', args=[999])  # Non-existent event ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_events_unauthenticated(self):
        # Test listing events without authentication
        list_url = reverse('events-list')
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_event_unauthenticated(self):
        # Test creating an event without authentication
        list_url = reverse('events-list')
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        data = {
            'name': 'Dinner Party',
            'occasion': self.occasion.id,
            'expender': self.user.id,
            'total_amount': 200,
            'utilizers_data': [{'utlizer': self.user.id, 'amount': 100}]
        }
        response = self.client.post(list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_event_unauthenticated(self):
        # Test retrieving an event without authentication
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = reverse('events-detail', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_event_unauthenticated(self):
        # Test updating an event without authentication
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = reverse('events-detail', args=[self.event.id])
        data = {
            'name': 'Updated Cake Cutting',
            'occasion': self.occasion.id,
            'expender': self.user.id,
            'total_amount': 150,
            'utilizers_data': [{'utlizer': self.user.id, 'amount': 75}]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_unauthenticated(self):
        # Test deleting an event without authentication
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = reverse('events-detail', args=[self.event.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_payments_unauthenticated(self):
        # Test retrieving payments for an event without authentication
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        url = reverse('events-payments', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class UtilizerViewSetTests(BaseTestCase):
    def test_create_utilizers(self):
        # Test creating utilizers
        create_url = reverse('utilizer-list')
        data = [
            {'event': self.event.id, 'utlizer': self.user.id, 'amount': 50}
        ]
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['amount'], '50.00')

    def test_create_utilizers_with_multiple_entries(self):
        # Test creating multiple utilizers
        create_url = reverse('utilizer-list')
        another_user = User.objects.create_user(email='another@example.com', password='testpassword')
        data = [
            {'event': self.event.id, 'utlizer': self.user.id, 'amount': 50},
            {'event': self.event.id, 'utlizer': another_user.id, 'amount': 50}
        ]
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)

    # Failure Test Cases

    def test_create_utilizers_with_missing_event(self):
        # Test creating utilizers with missing event ID
        create_url = reverse('utilizer-list')
        data = [
            {'utlizer': self.user.id, 'amount': 50}
        ]
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_utilizers_with_invalid_event(self):
        # Test creating utilizers with invalid event ID
        create_url = reverse('utilizer-list')
        data = [
            {'event': 999, 'utlizer': self.user.id, 'amount': 50}  # Non-existent event ID
        ]
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_utilizers_with_invalid_data(self):
        # Test creating utilizers with invalid data
        create_url = reverse('utilizer-list')
        data = [
            {'event': self.event.id, 'utlizer': self.user.id, 'amount': 'invalid_amount'}  # Invalid amount
        ]
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_utilizers_with_non_list_data(self):
        # Test creating utilizers with non-list data
        create_url = reverse('utilizer-list')
        data = {'event': self.event.id, 'utlizer': self.user.id, 'amount': 50}  # Not a list
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_utilizers_unauthenticated(self):
        # Test creating utilizers without authentication
        create_url = reverse('utilizer-list')
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        data = [
            {'event': self.event.id, 'utlizer': self.user.id, 'amount': 50}
        ]
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class PaymentViewSetTests(BaseTestCase):

    def test_list_payments(self):
        # Test listing payments made and received by the user
        list_url = reverse('payment-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_clear_expense(self):
        # Test clearing an expense for an event
        clear_expense_url = reverse('payment-clear-expense')
        print('user2', self.user2.id)
        print('user1', self.user.id)
        data = {
            'payer': self.user2.id,
            'payee': self.user.id,
            'event': self.event.id,
            'amount': 25
        }

        print("data==============>", data)
        response = self.client.post(clear_expense_url, data, format='json')
        print("response===================>", response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['amount'], '25.00')

  
    # # Failure Test Cases

    def test_clear_expense_with_missing_fields(self):
        # Test clearing an expense with missing required fields
        clear_expense_url = reverse('payment-clear-expense')
        data = {
            'payer': self.user2.id,
            'payee': self.user.id,
            'event': self.event.id
            # Missing 'amount'
        }
        response = self.client.post(clear_expense_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clear_expense_with_invalid_event(self):
        # Test clearing an expense with an invalid event ID
        clear_expense_url = reverse('payment-clear-expense')
        data = {
            'payer': self.user2.id,
            'payee': self.user.id,
            'event': 999,  # Non-existent event ID
            'amount': 25
        }
        response = self.client.post(clear_expense_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_clear_expense_with_non_participant_payee(self):
        # Test clearing an expense with a payee who was not part of the event
        clear_expense_url = reverse('payment-clear-expense')
        another_user = User.objects.create_user(email='another@example.com', password='testpassword')
        data = {
            'payer': self.user.id,
            'payee': another_user.id,  # Payee not part of the event
            'event': self.event.id,
            'amount': 25
        }
        response = self.client.post(clear_expense_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clear_expense_with_no_outstanding_balance(self):
        # Test clearing an expense with no outstanding balance
        clear_expense_url = reverse('payment-clear-expense')
        data = {
            'payer': self.user2.id,
            'payee': self.user.id,
            'event': self.event.id,
            'amount': 50  # No outstanding balance to clear
        }
        response = self.client.post(clear_expense_url, data, format='json')
        print("response===========>", response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clear_expense_with_exceeding_amount(self):
        # Test clearing an expense with an amount exceeding the balance due
        clear_expense_url = reverse('payment-clear-expense')
        data = {
            'payer': self.user2.id,
            'payee': self.user.id,
            'event': self.event.id,
            'amount': 100  # Amount exceeds balance due
        }
        response = self.client.post(clear_expense_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_payments_unauthenticated(self):
        # Test listing payments without authentication
        list_url = reverse('payment-list')
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_clear_expense_unauthenticated(self):
        # Test clearing an expense without authentication
        clear_expense_url = reverse('payment-clear-expense')
        self.client.force_authenticate(user=None)  # Unauthenticate the client
        data = {
            'payer': self.user2.id,
            'payee': self.user.id,
            'event': self.event.id,
            'amount': 25
        }
        response = self.client.post(clear_expense_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

