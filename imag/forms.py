from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, Div, Reset, Layout, Button
from django.forms import DateInput, Textarea, NumberInput, Select, ModelChoiceField, ChoiceField

from lab.forms import ExtractionForm as LExtractionForm
from lab.forms import RecordForm as LRecordForm
from .models import Record, Extraction
from collections import OrderedDict

class ChoiceFieldnovalidate(ChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value):
        """Validate that the input is in self.choices."""
        pass

class RecordForm(LRecordForm):

    subexps = OrderedDict([('STM/AFM', ['LT-U', 'DUF']), ('Prepa', ['LT-U', 'LT-4', 'DUF']),
                           ('Maintenance', ['LT-U', 'DUF', 'LT-4']),
                           ('Topo', ['LT-4']), ('Spectro', ['DUF']), ('Atom-Manipulation', ['LT-4']),
                           ('Tunneling_measurement', ['LT-4'])])

    subexp = ChoiceFieldnovalidate(choices=[(ind, k) for ind, k in enumerate(subexps.keys())], label='Usage:', widget=Select(attrs={'class': 'subexpclass',}))


    class Meta(LRecordForm.Meta):
        model = Record
        fields = ['date_from', 'time_from',
                  'date_to', 'time_to',
                  'user',
                  'wu',
                  'group', 'project', 'experiment', 'remark']

        labels = {'wu': 'WU:', 'date_from': 'From:', 'time_from':'Time:',
                  'date_to': 'To:', 'time_to': 'Time:',
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
        self.helper.form_class = 'form-horizontal formclass'
        self.helper.form_id = 'form_id'
        self.helper.form_tag = True
        self.helper.layout = Layout(
                Div(
                    Row(
                        Column('date_from', css_class='form-group col-md-3'),
                        Column('time_from', css_class='form-group col-md-3'),
                        Column('experiment', css_class='form-group col-6'),
                        Div(css_class='w-100'),
                        Column('date_to', css_class='form-group col-md-3'),
                        Column('time_to', css_class='form-group col-md-3'),
                        Column('wu', css_class='form-group col-md-4 uocol'),
                        css_class='form-row'
                    ),
                    Row(Column('project', css_class='form-group col-md-8'),
                        Column('subexp', css_class='form-group col-md-4'),
                        css_class='form-row',
                    ),
                    Row(
                        Column('user', css_class='form-group col-md-5'),
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

    def clean_subexp(self):
        data = self.cleaned_data['subexp']
        if data == '':
            return None
        return list(self.subexps.keys())[int(data)]

