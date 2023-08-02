from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    date_created = models.DateField(auto_now_add=True, verbose_name="Date created")
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'poll_id': self.pk})

    def get_results_url(self):
        return reverse('results', kwargs={'poll_id': self.pk})

    def get_delete_url(self):
        return reverse('delete', kwargs={'poll_id': self.pk})

    def get_stop_url(self):
        return reverse('stop', kwargs={'poll_id': self.pk})

    def __str__(self):
        if len(self.title) > 20:
            return f"{self.title[:20]}..."
        else:
            return self.title

    def can_vote(self, user):
        user_votes = user.vote_set.all()
        query_set = user_votes.filter(poll=self)
        if query_set.count() == 0:
            return True
        return False

    def get_amount_votes(self):
        return str(self.vote_set.count())

    def get_results(self):
        results = {}
        for candidate in self.candidate_set.all():
            if candidate.get_candidate_votes:
                results[candidate.__str__()] = f"{((candidate.get_candidate_votes / self.get_amount_votes) * 100):.2f}"
            else:
                results[candidate.__str__()] = "0"
        return results



class Candidate(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Name")
    middle_name = models.CharField(max_length=100, verbose_name="Middle name")
    last_name = models.CharField(max_length=100, verbose_name="Last name")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(max_length=1, verbose_name="Gender")

    def __str__(self):
        return f"{self.name} {self.middle_name} {self.last_name}"

    def get_candidate_votes(self):
        return str(self.vote_set.count())


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.poll.__str__()} - {self.candidate.__str__()}"
