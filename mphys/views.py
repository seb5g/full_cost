from pathlib import Path
from lab.views import FilterRecord, Export, GetRecord, LoadHTMLData

from .models import Record
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
        if exp == 'PPMS':
            values = [(ind, f'{ind}h00') for ind in range(24)]
        else:
            values = [(0, 'Morning'), (1, 'Afternoon')]
        return values

class GetRecord(GetRecord):
    record_class = Record
    form_class = RecordForm
    activity = activity


    def validate_record(self, record, form):
        error = manage_time.is_range_intersecting_date_session(record, self.record_class)
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
        if data['experiment'] == 'PPMS':
            record.date_to = record.date_from
            record.time_from = 0
            if record.wu > 4:
                record.time_to = 1
            else:
                record.time_to = 0

        return record


