from rest_framework import serializers
from docu_query.models import Document, Query, Vote

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentVoteSerializer(serializers.ModelSerializer):
    total_upvotes = serializers.IntegerField()
    total_downvotes = serializers.IntegerField()
    user_vote = serializers.CharField()

    class Meta:
        model = Document
        fields = ['drive_id', 'name', 'content', 'created_date', 'relevance_score', 
                  'total_upvotes', 'total_downvotes', 'user_vote']
        

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = '__all__'
    

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'