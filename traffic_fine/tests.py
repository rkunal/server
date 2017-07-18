from django.test import TestCase
from .models import *
import json
# Create your tests here.
class TrafficFineListPageTest(TestCase):
	fixtures = ['traffic-city-api.json']

	def test_get(self):
		res=self.client.get('/api/traffic-fine/')
		self.assertEqual(res.status_code,200)
		response_data = json.loads(res.content)
		#print response_data['trafficFineCities']
		self.assertTrue(response_data['trafficFineCities'])
		self.assertEqual(response_data['trafficFineCities'][0]['id'], 1)
		self.assertEqual(response_data['trafficFineCities'][0]['name'], 'Delhi')

		