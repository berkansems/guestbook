from rest_framework.test import APITestCase
from rest_framework import status


class GuestBookAPITests(APITestCase):

    def test_create_entry(self):
        response = self.client.post('/api/entries/',
                                    {'name': 'John Doe', 'subject': 'Hello', 'message': 'This is a test message.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_entries(self):
        self.client.post('/api/entries/', {'name': 'Jane Doe', 'subject': 'Test Subject', 'message': 'Test Message'})
        response = self.client.get('/api/entries/list/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        self.client.post('/api/entries/', {'name': 'Berkan Şems', 'subject': 'Hello', 'message': 'First message'})
        self.client.post('/api/entries/', {'name': 'Ali şems', 'subject': 'Hello again', 'message': 'Second message'})
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_entry_missing_fields(self):
        # Test creating an entry with missing fields to check for validation errors
        response = self.client.post('/api/entries/', {'name': 'Incomplete Entry'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('subject', response.data)
        self.assertIn('message', response.data)

    def test_get_entry_detail(self):
        # Test retrieving a specific entry by its ID
        entry_response = self.client.post('/api/entries/', {'name': 'John Doe', 'subject': 'Detail Test',
                                                            'message': 'Testing entry detail retrieval.'})
        entry_id = entry_response.data['id']
        response = self.client.get(f'/api/entries/{entry_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], 'Detail Test')

    def test_pagination_entries_list(self):
        # Create multiple entries to test pagination
        for i in range(10):
            self.client.post('/api/entries/',
                             {'name': f'User {i}', 'subject': f'Subject {i}', 'message': f'Message {i}'})
        response = self.client.get('/api/entries/list/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('entries' in response.data)
        self.assertLessEqual(len(response.data['entries']), 3)

    def test_update_entry(self):
        # Test updating an existing entry
        entry_response = self.client.post('/api/entries/',
                                          {'name': 'Jane Doe', 'subject': 'Update Test', 'message': 'Original Message'})
        entry_id = entry_response.data['id']
        update_response = self.client.put(f'/api/entries/{entry_id}/',
                                          {'name': 'Jane Doe', 'subject': 'Updated Subject',
                                           'message': 'Updated Message'})
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['subject'], 'Updated Subject')
        self.assertEqual(update_response.data['message'], 'Updated Message')

    def test_delete_entry(self):
        # Test deleting an entry
        entry_response = self.client.post('/api/entries/', {'name': 'John Doe', 'subject': 'Delete Test',
                                                            'message': 'This entry will be deleted.'})
        entry_id = entry_response.data['id']
        delete_response = self.client.delete(f'/api/entries/{entry_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that entry no longer exists
        get_response = self.client.get(f'/api/entries/{entry_id}/')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
