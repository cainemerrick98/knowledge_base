from rest_framework import filters
from rest_framework.settings import api_settings
from docu_query.text_preprocessing import preprocess_text
from django.db.models import Count, Max, Case, When, CharField, Value

class QueryRelevanceFilter(filters.BaseFilterBackend):
    query_param = "query"
    user_param = "user"
    
    def get_query(self, request):
        """
        Extracts the query string from the url params
        and preprocesses it
        """
        query = request.query_params.get(self.query_param)
        return preprocess_text(query)
    
    def get_user(self, request):
        """
        Extracts the user email from the url params
        """
        user = request.query_params.get(self.user_param)
        return user
    
    def count_votes(self, queryset):
        queryset = queryset.annotate(
            total_upvotes = Count(Case(When(vote__vote_type="UP", then=1))),
            total_downvotes = Count(Case(When(vote__vote_type="DOWN", then=1)))
        )
        return queryset
    
    def user_vote(self, queryset, user):
        queryset = queryset.annotate(
            user_vote = Max(Case(
                When(vote__user=user, vote__vote_type='UP', then=Value('UP')),
                When(vote__user=user, vote__vote_type='DOWN', then=Value('DOWN')),
                default=None,
                output_field=CharField()
            ))
        )
        return queryset

    def filter_queryset(self, request, queryset, view):
        """
        Calculates the relevance score of each document given the query
        Returns the queryset ordered by relevance score.
        """
        query = self.get_query(request)
        user = self.get_user(request)

        relevance_calculator = getattr(view, 'relevance_calculator', None)
        if relevance_calculator is None:
            raise ValueError("Relevance calculator not set on the view")

        try:
            queryset = relevance_calculator().calculate_relevance(queryset, query)
        except ValueError:
            #There are no documents in the database
            return queryset
        
        queryset = self.count_votes(queryset)
        queryset = self.user_vote(queryset, user)
        return queryset.filter(relevance_score__gt=0.09).order_by('-relevance_score')
    
   
