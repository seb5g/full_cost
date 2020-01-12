from django.forms import ModelForm, DateInput, Textarea, NumberInput, Select, CharField, TextInput, ModelChoiceField, ChoiceField
from .models import Record, Experiment, WorkOn
from lab.forms import RecordForm as LRecordForm


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Submit, Row, Column, Div, Reset, Layout, Button
from crispy_forms.bootstrap import FormActions

class RecordForm(LRecordForm):

    class Meta(LRecordForm.Meta):
        model = Record
        fields = ['date_from', 'time_from', 'time_to',
                  'user',
                  'wu', 'finished',
                  'group', 'project', 'experiment', 'remark', 'workon']

        labels = {'wu': 'WU:', 'date_from': 'Date:', 'time_from':'From:',
                  'date_to': 'To:', 'time_to': 'To:',
                  'experiment': 'Worker:',
                  'finished': 'Finished',
                  'workon': 'Working on:'
                  }

        help_texts = {'date_from': 'The date of your run',
                      'time_from': 'The first session of your run',
                      'time_to': 'The last session of your run',
                      'experiment': 'Worker:',
                      'workon': 'Select a project you are working on:',
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
            'wu' : NumberInput(attrs = {'required': False, 'class': 'uo', 'value': 0, 'min': 0, 'step':0.5,'style': 'width:10ch',}),
            'workon': Select(attrs={'class': 'workon'}),

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
                        Column('workon', css_class='form-group col-8 uocol'),
                        Column('finished', css_class='form-group col-4 uocol'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('date_from', css_class='form-group col-4'),
                        Column('time_from', css_class='form-group col-4'),
                        Column('time_to', css_class='form-group col-4'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('experiment', css_class='form-group col-6'),
                        Column('wu', css_class='form-group col-6 uocol' ),
                    ),

                    Row(
                        Column('project', css_class='form-group col-md-12'),
                    ),
                    Row(
                        Column('user', css_class='form-group col-md-5 mr-2'),
                        Column('user_text_name', css_class='form-group col-md-3 usercol'),
                        Column('user_text_surname', css_class='form-group col-md-3 usercol'),
                        Column('group', css_class='form-group col-md-4'),
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

        self.fields['workon'].queryset = WorkOn.objects.filter(finished=False)
