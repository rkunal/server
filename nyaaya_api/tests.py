from django.test import TestCase
from law.models import *
import json
# Create your tests here.
class CatalogueByCategories(TestCase):
	fixtures = ['catalogue_testdata.json']

	def test_get(self):
		res=self.client.get('/api/catalogue/category/')
		self.assertEqual(res.status_code,200)
		self.assertEqual(res.accepted_media_type, 'application/json')
		response_data = json.loads(res.content)
		self.assertTrue(response_data['catalogueitems'])
		self.assertEqual(response_data['catalogueitems'][0]['id'],12)
		self.assertEqual(response_data['catalogueitems'][0]['name'] ,'Accountability laws')
		

class CatalogueForCategory(TestCase):
    fixtures = ['catalogue_testdata.json']

    def test_get(self):
        res=self.client.get('/api/catalogue/category/12/slug/')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.accepted_media_type,'application/json')
        response_data = json.loads(res.content)
        self.assertTrue(response_data['catalogueitems'])
        self.assertEqual(response_data['catalogueitems'][0]['id'], 235)
        self.assertEqual(response_data['catalogueitems'][0]['name'],'Karnataka Laws')

class CatalogueByJurisdiction(TestCase):
    fixtures = ['catalogue_testdata.json']

    def test_get(self):
        res=self.client.get('/api/catalogue/jurisdiction/')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.accepted_media_type,'application/json')
        response_data = json.loads(res.content)
        self.assertTrue(response_data['catalogueitems'])
        self.assertEqual(response_data['catalogueitems'][0]['id'], 235)
        self.assertEqual(response_data['catalogueitems'][0]['name'],'Karnataka Laws')
    
class CatalogueForCateoryForJurisdiction(TestCase):
    fixtures = ['catalogue_testdata.json']

    def test_get(self):
        res=self.client.get('/api/catalogue/category/12/category_slug/jurisdiction/235/jurisdiction_slug/')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.accepted_media_type,'application/json')
        response_data = json.loads(res.content)
        self.assertTrue(response_data['catalogueitems'])
        self.assertEqual(response_data['catalogueitems'][0]['id'], 3)
        self.assertEqual(response_data['catalogueitems'][0]['name'],'The Central Vigilance Commission Act, 2003')
        self.assertEqual(response_data['catalogueitems'][0]['locality'],'Karnataka')
        self.assertEqual(response_data['catalogueitems'][0]['document_id'], 480)


    

class CatalogueForJurisdiction(TestCase):
    fixtures = ['catalogue_testdata.json']

    def test_get(self):
        res=self.client.get('/api/catalogue/jurisdiction/235/jurisdiction_slug/')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.accepted_media_type,'application/json')
        response_data = json.loads(res.content)
        self.assertTrue(response_data['catalogueitems'])
        self.assertEqual(response_data['catalogueitems'][0]['id'], 12)
        self.assertEqual(response_data['catalogueitems'][0]['name'],'Accountability laws')

class CatalogueForJurisdictionForCateory(TestCase):
    fixtures = ['catalogue_testdata.json']

    def test_get(self):
        res=self.client.get('/api/catalogue/jurisdiction/235/jurisdiction_slug/category/12/category_slug/')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.accepted_media_type,'application/json')
        response_data = json.loads(res.content)
        self.assertTrue(response_data['catalogueitems'])
        self.assertEqual(response_data['catalogueitems'][0]['id'], 3)
        self.assertEqual(response_data['catalogueitems'][0]['name'],'The Central Vigilance Commission Act, 2003')
        self.assertEqual(response_data['catalogueitems'][0]['locality'],'Karnataka')
        self.assertEqual(response_data['catalogueitems'][0]['document_id'], 480)

class GuideIntro(TestCase):
    fixtures = ['catalogue_testdata.json']

    def test_get(self):
        res=self.client.get('/api/law-explainers/3/slug/')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.accepted_media_type,'application/json')
        response_data = json.loads(res.content)
        self.assertTrue(response_data['guide_intro'])
        self.assertEqual(response_data['guide_intro']['data'],'This is some random text added for testing')
        self.assertEqual(response_data['guide_intro']['short_title'],'The Central Vigilance Commission Act, 2003')


class LawExplainersPageTest(TestCase):
    fixtures=['AppTocExplainer.json']

    def test_get(self):
        res=self.client.get('/api/law-explainers/')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.accepted_media_type,'application/json')
        response_data = json.loads(res.content)
        self.assertTrue(response_data['explainers'])
        self.assertEqual(response_data['explainers'][1]['title'],'Delay in possession by builder/developer')
        self.assertEqual(response_data['explainers'][1]['url'],'/guide-3/law-explainers/')
        self.assertEqual(response_data['explainers'][2]['image_desktop'],"pyramid_app/toc/illustrations/cb2cdb4b-b541-4add-a660-9686b8d5812d.desktop.JPG")
        self.assertEqual(response_data['explainers'][2]['url'],'/guide-3/law-explainers-2/')
        self.assertEqual(response_data['explainers'][3]['image_desktop'],"pyramid_app/toc/illustrations/a1e1e18d-7f21-484a-a275-261b5f86181e.desktop.JPG")

        



