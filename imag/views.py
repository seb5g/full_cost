from pathlib import Path
from lab.views import FilterRecord, Export, GetRecord, LoadExperiments, LoadHTMLData
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

class LoadHTMLData(LoadHTMLData):
    """view used to modify dynamically the content of the field time_to or time_from in the record form.
     The ajax call to this view is configured within the dedicated javascript file, see static"""
    def set_values(self, request):
        exp = request.GET.get('exp')
        subexps = RecordForm.subexps
        values = []
        if exp is not None:
            for ind, k in enumerate(subexps.keys()):
                for val in subexps[k]:
                    if val in exp:
                        values.append((ind, k))
        return values


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

        if data.get('subexp'):
            remark_tmp = record.remark
            subexp = data.get('subexp')
            record.remark = subexp + ' / ' + remark_tmp
        return record
