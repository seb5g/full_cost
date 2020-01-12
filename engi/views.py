from pathlib import Path
from lab.views import FilterRecord, Export, GetRecord
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from .models import Record, WorkOn
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

class SetWorkoN(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'engi:grecord'


class GetRecord(GetRecord):
    record_class = Record
    form_class = RecordForm
    activity = activity

    def validate_record(self, record, form):
        records = Record.objects.filter(experiment__exact=record.experiment, date_from=record.date_from)
        error = manage_time.is_range_intersecting_session(record, records)
        if error is not None:
            form.add_error(None, error)

        if form.is_valid():
            form.cleaned_data['workon'].finished = form.cleaned_data['finished']
            form.cleaned_data['workon'].save()

        validate_state = True
        return form, validate_state

    def get_workon(self, workon_id):
        if workon_id is None or workon_id == '':
            return None
        else:
            workon = WorkOn.objects.get(id=int(workon_id))
        return workon

    def form_class_init(self,request, **kwargs):
        ini_dict = kwargs
        workon = self.get_workon(request.GET.get('workon'))
        if workon is not None:
            project = workon.project
            user = workon.user
            group = workon.user.group
            ini_dict.update({'workon': workon, 'user': user, 'project': project, 'group': group})
        return self.form_class(initial=ini_dict)