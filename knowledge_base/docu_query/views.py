from rest_framework import generics, status
from rest_framework.response import Response
from docu_query.models import Document, Query, Vote
from docu_query.serializers import DocumentSerializer, DocumentVoteSerializer, VoteSerializer
from docu_query.filters import QueryRelevanceFilter
from docu_query.relevance_calculators import TFIDFCosineSimilarityCalculator

class UploadDocumentView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Creates a document if the serialiser is valid. Serialiser just expects
        all fields to be non empty i.e. the request data has a value for each 
        column in the database. 
        Content is preprocessed using the preprocess_text function and then saved
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, 
                            status=status.HTTP_201_CREATED, headers=headers)

        return Response(
            {'error':serializer.errors,
             'success':False}, 
            status=status.HTTP_400_BAD_REQUEST, )

    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
class QueryDocumentView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentVoteSerializer
    filter_backends = [QueryRelevanceFilter]
    relevance_calculator = TFIDFCosineSimilarityCalculator

    def list(self, request, *args, **kwargs):
        self.save_query(request)
        return super().list(request, *args, **kwargs)

    def save_query(self, request):
        query = request.query_params.get('query')
        Query.objects.create(query=query)

class VoteDocumentView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Creates the vote if the serialiser is valid. The vote serialiser
        expects the request to have a data attribute that contains key values
        for all of the fields in the vote model
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, 
                            status=status.HTTP_201_CREATED, headers=headers)
        
        
        elif 'non_field_errors' in serializer.errors:
            """
            The serializer was not valid because this user has already voted on this document
            hence we need to update this vote with the new vote type and save the vote.
            We also need to differentiate between the the vote type being changed or not. We will use
            the status code to reflect this.
            """
            user = request.data.get('user')
            document = request.data.get('document')
            vote = Vote.objects.filter(user=user, document=document)[0]
            headers = self.get_success_headers(serializer.data)
            if vote.vote_type == request.data.get('vote_type'):
                """
                If the user has casted the same vote they previously casted on 
                the document
                """
                return Response(serializer.data, 
                            status=status.HTTP_200_OK, headers=headers)

            else:
                """
                If the user has voted on the document before and they have changed their
                vote we need to update the vote type on vote and then respond.
                """
                vote.vote_type = request.data.get('vote_type')
                vote.save()
                return Response(serializer.data, 
                            status=status.HTTP_202_ACCEPTED, headers=headers)
        
                    
        return Response(
            {'error':serializer.errors,
             'success':False}, 
            status=status.HTTP_400_BAD_REQUEST)


    







        
        

        
    

    
