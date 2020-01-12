from django.forms import  DateInput, Textarea, NumberInput, Select, MultipleChoiceField, CheckboxSelectMultiple, ModelChoiceField
from .models import Record
from lab.models import Extraction
from lab.forms import RecordForm as LRecordForm
from lab.forms import ExtractionForm as LExtractionForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, Div, Reset, Layout, Button
from crispy_forms.bootstrap import FormActions

class RecordForm(LRecordForm):

    class Meta(LRecordForm.Meta):
        model = Record
        fields = ['date_from', 'time_from',
                  'date_to', 'time_to',
                  'user',
                  'wu',
                  'group', 'project', 'experiment', 'remark']

        labels = {'wu': 'WU:', 'date_from': 'From:', 'time_from':'Time from:',
                  'date_to': 'To:', 'time_to': 'Time to:',
                  'experiment': 'Experiment:',
                  }

        help_texts = {'date_from': 'The starting date of your run',
                      'date_to': 'The last date of your run',
                      'time_from': 'The first session of your run',
                      'time_to': 'The last session of your run',
                      'experiment': 'Pick an experiment'
                      }

        widgets = {
            'date_from' : DateInput(attrs={'type':'date', 'class':'datepicker dfrom time'}),
            'date_to' : DateInput(attrs={'type':'date', 'class':'datepicker dto time'}),
            'time_to' : Select(attrs={'class': 'tto time'}),
            'time_from': Select(attrs={'class': 'tfrom time'}),
            'remark' : Textarea(attrs={'placeholder': 'Enter some detail here about your experiment',
                                       'rows': '1', 'cols' :'50'}),
            'experiment': Select(attrs={'class': 'experiment', }),
            'group': Select(attrs={'class': 'group', }),
            'project': Select(attrs={'class': 'project', }),
            'user' : Select(attrs = {'placeholder': 'Surname Name', 'class': 'user'}),
            'wu' : NumberInput(attrs = {'required': False, 'class': 'uo', 'value': 0, 'min': 0, 'step':0.5,'style': 'width:10ch'}),
        }
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.help_text_inline = False
        self.helper.form_class = 'form-inline formclass  mw-100'
        self.helper.form_id = 'form_id'
        self.helper.form_tag = True
        self.helper.layout = Layout(
                Div(
                    Row(
                        Column('date_from', css_class='form-group col-md-3'),
                        Column('time_from', css_class='form-group col-md-3 timecol'),
                        Column('wu', css_class='form-group col-md-6 uocol' ),
                        Div(css_class='w-100'),
                        Column('date_to', css_class='form-group col-md-3 timecol'),
                        Column('time_to', css_class='form-group col-md-3 timecol'),
                        Column('experiment', css_class='form-group col-md-6'),
                        css_class='form-row'
                    ),
                    Row('project'),
                    Row(
                        Column('user', css_class='form-group col-md-6'),
                        Column('user_text_name', css_class='form-group col-md-3 usercol'),
                        Column('user_text_surname', css_class='form-group col-md-3 usercol'),
                        Column('group', css_class='form-group col-md-2'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('remark', css_class='form-group mr-5'),
                        Column(FormActions(
                                        Button('okbutton', 'Submit', css_class='btn-primary okclass'), #form will be triggered using a popup jquery, see static/js/osp_records.js
                                        Reset('name', 'Reset', css_class='btn-secondary')
                                            ),css_class='form-group align-items-center')
                        ),
            )
        )

        super().__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                if 'class' in self.fields[field].widget.attrs:
                    self.fields[field].widget.attrs['class'] += ' has-popover'
                self.fields[field].widget.attrs.update(
                    {'data - toggle': 'popover',
                     'data-content': help_text, 'data-placement': 'right',
                     'data-container': 'body'})


