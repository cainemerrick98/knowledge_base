from django.db import models

class Query(models.Model):
    query = models.CharField(max_length=500, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query


class Document(models.Model):
    drive_id = models.CharField(primary_key=True, max_length=100, blank=False)
    name = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=False)
    created_date = models.DateField(auto_now_add=True, null=True)
    relevance_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
    def set_relevance_score(self, score):
        self.relevance_score = score
        self.save()


class Vote(models.Model):
    voteType = models.TextChoices('VoteType', 'UP DOWN')
    
    user = models.CharField(max_length=256, blank=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, blank=False)
    vote_type = models.CharField(choices=voteType, max_length=4, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        unique_together = ['user', 'document']
        indexes = [
            models.Index(fields=['user', 'document'])
        ]

    def __str__(self):
        return f'{self.user} {self.document} {self.vote_type} {self.timestamp}'



    
