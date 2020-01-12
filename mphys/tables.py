# tutorial/tables.py
import lab.tables as tables
from .models import Record

Rfields = [f.name for f in Record._meta.fields]

class RecordTable(tables.RecordTable):
    class Meta(tables.RecordTable.Meta):
        model = Record


class RecordTableFull(tables.RecordTableFull):
    class Meta(tables.RecordTableFull.Meta):
        model = Record
        fields = tuple(Rfields)
        exclude = ('nights',)
        sequence = [f for f in tables.field_sequence if f in Rfields]+['...']

