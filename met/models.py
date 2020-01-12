from pathlib import Path
from full_cost.utils.constants import ACTIVITIES

from django.db import models
from lab.models import Record as LRecord
from lab.models import Extraction
from lab.models import Record2Range, RecordDate
from simple_history.models import HistoricalRecords

activity_short = Path(__file__).parts[-2]

sub_billings = ACTIVITIES[activity_short]['sub_billings']



class Experiment(models.Model):
    exp_type = models.CharField(choices=sub_billings, default=sub_billings[0][0], max_length=200)
    experiment = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.experiment} ({self.get_exp_type_display()})'

# class Extraction(Extraction):
#     history = HistoricalRecords()

class Record(LRecord, RecordDate, Record2Range):
    nights = models.PositiveIntegerField(default=0)
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
                f'{self.experiment} from {self.date_from}/{self.time_from} to {self.date_to}/{self.time_to}'
        except:
            return 'Null record'


