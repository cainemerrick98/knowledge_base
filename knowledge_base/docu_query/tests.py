from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from docu_query.models import Document, Query, Vote
from docu_query.text_preprocessing import preprocess_text

# Create your tests here.
class UploadDocumentViewTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('upload')
        self.data = {
            'name':'test_file_name',
            'content':'test_content',
            'drive_id':'iejfe93874',
        }
    
    def test_upload_document_with_data(self):
        resp = self.client.post(self.url, self.data)
        
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(len(Document.objects.all()), 1)
        

    def test_upload_document_without_data(self):
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, 400)
    
class QueryDocumentViewTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('query')
        self.query = 'test query'
        self.user = 'caine.merrick@pwc.com'
        self.url += f'?query={self.query}&user={self.user}'

    def test_save_query(self):
        self.client.get(self.url)
        saved_query = Query.objects.first()

        self.assertEqual(Query.objects.count(), 1)
        self.assertEqual(saved_query.query, self.query)

    def test_list_documents(self):
        Document.objects.create(name='test_1', content='test content for content on the drive might match a query who knows if the query will return a query test', drive_id='aaa')
        Document.objects.create(name='test_2', content='test content test test content', drive_id='bbb')

        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 2)
        self.assertEqual(Query.objects.count(), 1)

    def test_count_document_votes(self):
        document = Document.objects.create(name='test_2', content='test content test test content', drive_id='bbb')
        Vote.objects.create(user='caine.merrick@pwc.com', document=document, vote_type='UP')
        Vote.objects.create(user='caine.merrick2@pwc.com', document=document, vote_type='DOWN')
        Vote.objects.create(user='caine.merrick3@pwc.com', document=document, vote_type='UP')

        resp = self.client.get(self.url)
        self.assertEqual(resp.data[0]['total_upvotes'], 2)
        self.assertEqual(resp.data[0]['total_downvotes'], 1)

    def test_user_vote(self):
        document = Document.objects.create(name='test_2', content='test content test test content', drive_id='bbb')
        Vote.objects.create(user='caine.merrick@pwc.com', document=document, vote_type='UP')
        Vote.objects.create(user='caine.merrick2@pwc.com', document=document, vote_type='DOWN')
        Vote.objects.create(user='caine.merrick3@pwc.com', document=document, vote_type='UP')

        resp = self.client.get(self.url)
        self.assertEqual(resp.data[0]['user_vote'], 'UP')

class VoteDocumentViewTest(APITestCase):
    
    def setUp(self) -> None:
        self.url = reverse('vote')
        self.data = {
            'document':'iejfe93874',
            'vote_type':'UP',
            'user':'caine.merrick@pwc.com'
        }

    def test_vote_with_data(self):
        Document.objects.create(name='test_1', content='test content', drive_id='iejfe93874')        
        resp = self.client.post(self.url, self.data)

        self.assertEqual(resp.status_code, 201)

        doc = Document.objects.get(pk='iejfe93874')
        votes = doc.vote_set.all()
        up_votes = votes.filter(vote_type='UP')
        down_votes = votes.filter(vote_type='DOWN')
        
        self.assertEqual(len(votes), 1)
        self.assertEqual(len(up_votes), 1)
        self.assertEqual(len(down_votes), 0)
        
    def test_vote_without_data(self):
        resp = self.client.post(self.url, {})
        self.assertEqual(resp.status_code, 400)

    def test_vote_unique_together_constraint_different_vote(self):
        Document.objects.create(name='test_1', content='test content', drive_id='iejfe93874')
        doc = Document.objects.get(pk='iejfe93874')
        Vote.objects.create(document=doc, vote_type='DOWN', user='caine.merrick@pwc.com')
        vote = doc.vote_set.all()[0]
        self.assertEqual(vote.vote_type, 'DOWN')
        
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 202)
        
        #vote should have been changed to up
        vote = doc.vote_set.all()[0]
        self.assertEqual(vote.vote_type, 'UP')

    def test_vote_unique_together_constraint_same_vote(self):
        Document.objects.create(name='test_1', content='test content', drive_id='iejfe93874')
        doc = Document.objects.get(pk='iejfe93874')
        Vote.objects.create(document=doc, vote_type='UP', user='caine.merrick@pwc.com')
        vote = doc.vote_set.all()[0]
        self.assertEqual(vote.vote_type, 'UP')
        
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 200)
        
        #vote should still be up
        vote = doc.vote_set.all()[0]
        self.assertEqual(vote.vote_type, 'UP')

class TextPreprocessingTest(TestCase):
    
    def test_process_document_content(self):

        content = 'This is an example of some content. Something about PwC and something else.'
        expected_ouput = 'example content something pwc something else'

        preprocessed_content = preprocess_text(content)

        self.assertEqual(expected_ouput, preprocessed_content)


    
    
    

        


