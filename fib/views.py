from pathlib import Path
from lab.views import FilterRecord, Export, GetRecord, LoadExperiments, LoadSessions, LoadHTMLData
from django.shortcuts import render
from .models import Record, Experiment
from .forms import RecordForm
from .tables import RecordTable, RecordTableFull
from .filters import RecordFilter
from full_cost.utils import manage_time
from full_cost.utils.constants import ACTIVITIES
#####################################################
activity_short = Path(__file__).parts[-2]
activity_long = ACTIVITIES[activity_short]['activity_long']
activity={'short': activity_short, 'long': activity_long,}
#####################################################

class FilterRecord(FilterRecord):
    filter_class = RecordFilter
    table_class = RecordTable
    activity = activity

class Export(Export):
    table_class = RecordTableFull
    activity = activity


class LoadExperiments(LoadExperiments):
    """view used to modify dynamically the content of the field experiment in the record form.
     The ajax call to this view is configured within the dedicated javascript file, see static"""
    def set_experiments(self, request):
        fib = request.GET.get('fib')
        experiments = Experiment.objects.filter(fib_name=fib)
        return experiments

class LoadSessions(LoadSessions):
    """view used to modify dynamically the content of the field time_to or time_from in the record form.
     The ajax call to this view is configured within the dedicated javascript file, see static"""
    def set_sessions(self, request):
        fib = request.GET.get('fib')
        if fib == 'HELIOS':
            sessions = Record._meta.get_field('time_to').choices
        else:
            sessions = Record._meta.get_field('time_to').choices[0:-1]
        return sessions


class GetRecord(GetRecord):
    record_class = Record
    form_class = RecordForm
    activity = activity


    def validate_record(self, record, form):
        records = Record.objects.filter(experiment__exact=record.experiment, date_from=record.date_from)
        error = manage_time.is_range_intersecting_session(record, records)
        if error is not None:
            form.add_error(None, error)
        validate_state = True
        return form, validate_state

    def populate_record(self, data):
        """to be eventually subclassed"""
        # populate a new record
        # billing field should be populated depending on each activity cases (so in subclasses)
        record = self.record_class()
        for key in data:
            if hasattr(self.record_class, key):
                setattr(record, key, data[key])

        return record
