from pathlib import Path
from full_cost.utils.constants import ACTIVITIES
from django.db import models
from lab.models import Record as LRecord
from lab.models import Extraction, User, Project
from lab.models import Record4Range, RecordOneDate
from simple_history.models import HistoricalRecords

activity_short = Path(__file__).parts[-2]

sub_billings = ACTIVITIES[activity_short]['sub_billings']

class Experiment(models.Model):
    experiment = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Worker')
    exp_type = models.CharField(choices=sub_billings, default=sub_billings[0][0], max_length=200)
    #worker =models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.experiment}'

class WorkOn(models.Model):
    workon = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True,)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.workon}'

class Record(LRecord, RecordOneDate, Record4Range):
    workon = models.ForeignKey(WorkOn, on_delete=models.SET_NULL, blank=True, null=True,)
    finished = models.BooleanField(default=False)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    extraction = models.ForeignKey(Extraction, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="%(app_label)s_%(class)s_related",
                                   related_query_name="%(app_label)s_%(class)ss",
                                   )
    history = HistoricalRecords()

    def __str__(self):
        sub = self.submitted.strftime('%Y-%m-%d')
        try:
            return f'{activity_short} record {self.id} submitted the {sub}: {self.user} used '+\
                f'{self.experiment} the {self.date_from} {self.time_from}'
        except:
            return 'Null record'


