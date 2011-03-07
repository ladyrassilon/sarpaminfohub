import django_tables as tables
from sarpaminfohub.infohub.sarpam_table import SarpamTable
from django.template.loader import render_to_string

class FormulationTable(SarpamTable):
    country = tables.Column()
    fob_price = tables.Column(verbose_name="FOB Price")
    landed_price = tables.Column(verbose_name="Landed Price")
    rows_template = "formulation_rows.html"
    max_price = 0

    def __init__(self, rows):
        for row in rows:
            self.round_to_three_decimal_places(row, 'fob_price')
            self.round_to_three_decimal_places(row, 'landed_price')

            if isinstance(row['fob_price'], float) and row['fob_price'] > self.max_price:
                self.max_price = row['fob_price']

            if isinstance(row['landed_price'], float) and row['landed_price'] > self.max_price:
                self.max_price = row['landed_price']

        tables.MemoryTable.__init__(self, rows)

    def as_html(self):
        return render_to_string('table.html',\
                                {'table':self})

    def as_graph(self):
        return render_to_string('formulation/graph.html',\
                                {'table':self})
