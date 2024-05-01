# Knowledge Base

A DJango rest framework API for transforming a collection of documents (e.g. a google drive) into a searchable knowledge base.

Queries are matched to documents using the cosine similarity between the TFIDF of the query and each document with stop words removed. Other relevance calculator can be added by subsclassing the base relevance calculator and exposing a calculate relevance method.

Users can vote on documents if the front end exposes the voting api. The backend is already set up to handle the same user voting twice or switching their vote and responds appropiately. 

