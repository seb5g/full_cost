"""
CEMES organisation
People enter their working units per activity => one database per activity
Admins make an invoice per facturation => one bill use entries possibly from various databases or an inset of databases
"""
CNRS_PERCENTAGE = 6

ACTIVITIES ={'osp': {'activity_short': 'osp', 'activity_long': 'Optical Spectrocopy Platform',
                                            'sub_billings': [('SPEC','Optical Spectroscopy')],
                     'related_entities': {'SPEC': 'SPECTRO'}},

             'met': {'activity_short': 'met', 'activity_long': 'Transmission Electron Microscopy Platform',
                     'sub_billings': [('METC','Conventionnal TEM'), ('META', 'Advanced TEM')],
                     'related_entities': {'META': 'TEM', 'METC': 'TEM'}},

             'prepa': {'activity_short': 'prepa', 'activity_long': 'Sample Preparation Service',
                                            'sub_billings': [('PREPC','Conventionnal Preparation'),
                                                            ('FIBp','FIB preparation'),
                                                             ('SOFT','Soft Matter'),],
                     'related_entities': {'PREPC': 'PREPA', 'PREPF': 'PREPA'}},

             'fib': {'activity_short': 'fib', 'activity_long': 'Focused Ion Beam', 'sub_billings':
                                                    [('FIBp','FIB preparation'),
                                                     ('MEBA','Advanced MEB'),
                                                     ('FIBc','FIB Clean Room'),],
                     'related_entities': {'FIBp': 'PREPA', 'MEBA': 'MEBA', 'FIBc': 'FIBCR', }},

             'mphys': {'activity_short': 'mphys', 'activity_long': 'PS2I','sub_billings':
                                                [('MAG', 'Magnetic Measurement'),
                                                 ('MATC', 'Material Caracterisation')],
                    'related_entities': {'MAG': 'MAGNETIC', 'MATC': 'MATCARAC'}},
            'chem':{'activity_short': 'chem', 'activity_long': 'Chemistry','sub_billings': [('CHEM', 'Chemistry'),],
                     'related_entities': {'CHEM': 'CHEM'}},

            'imag': {'activity_short': 'imag', 'activity_long': 'Local Imagery',
                     'sub_billings': [('UHVI', 'UHV Imagery'),
                                      ('LT4', 'LT-UHV 4 tips'),
                                      ('NEARF', 'Near-field microscopy'),],
                      'related_entities': {'UHVI': 'UHVI', 'LT4': 'LT4', 'NEARF':'NEARF'}},
            'fab': {'activity_short': 'fab', 'activity_long': 'Nanomaterial Fabrication',
                            'sub_billings': [('CLEANR', 'Clean Room Processes'),
                                             ('DUFG', 'Growth DUF'),
                                             ('GROWTH', 'Growth'),
                                             ('IMPLANT', 'Ionic Implantation')],
                      'related_entities': {'CLEANR': 'CLEANR', 'DUFG': 'DUFG',
                                           'GROWTH': 'GROWTHIMP', 'IMPLANT': 'GROWTHIMP'}},
             'engi': {'activity_short': 'engi', 'activity_long': 'Engineering Platform',
                     'sub_billings': [('MECA', 'Mechanic Service'),
                                      ('ELEC', 'Electronic Service'),],
                     'related_entities': {'MECA': 'MECA', 'ELEC': 'ELEC',}},
             }
activities_choices = [(k, ACTIVITIES[k]['activity_long'],) for k in ACTIVITIES.keys()]

BILLINGS = [dict(entity=('SPECTRO', 'Optical Spectroscopy'), activities=('osp',),
                            related_subbillings=[dict(short='SPEC', long='Optical Spectroscopy')]),
                dict(entity=('TEM', 'Electronic Microscopy'), activities=('met',),
                     related_subbillings=[dict(short='META', long='Advanced TEM'),dict(short='METC', long='Conventionnal TEM')],),
                dict(entity=('PREPA', 'Sample Preparation'), activities=('prepa', 'fib'),
                     related_subbillings=[dict(short='PREPC', long='Conventionnal Preparation'), dict(short='FIBp', long='FIB preparation')],),
                dict(entity=('MEBA', 'Advanced MEB'), activities=('fib',),
                     related_subbillings=[dict(short='MEBA', long='Advanced MEB')],),
                dict(entity=('FIBCR', 'FIB Clean Room'), activities=('fib',),
                     related_subbillings=[dict(short='FIBc', long='FIB Clean Room')],),
                dict(entity=('SOFT', 'Soft Matter'), activities=('prepa',),
                     related_subbillings=[dict(short='SOFT', long='Soft Matter')],),
                dict(entity=('MATCARAC', 'Material Caracterisation'), activities=('mphys',),
                      related_subbillings=[dict(short='MATC', long='Material Caracterisation')],),
                dict(entity=('MAGNETIC', 'Magnetic Measurement'), activities=('mphys',),
                      related_subbillings=[dict(short='MAG', long='Magnetic Measurement')],),
                dict(entity=('CHEM', 'Chemistry'), activities=('chem',),
                    related_subbillings=[dict(short='CHEM', long='Chemistry')],),
                dict(entity=('CLEANR', 'Clean Room Processes'), activities=('fab',),
                      related_subbillings=[dict(short='CLEANR', long='Clean Room Processes')],),
                dict(entity=('UHVI', 'UHV Imagery'), activities=('imag',),
                      related_subbillings=[dict(short='UHVI', long='UHV Imagery')],),
                dict(entity=('LT4', 'LT-UHV 4 tips'), activities=('imag',),
                      related_subbillings=[dict(short='LT4', long='STM 4tips')],),
                dict(entity=('DUFG', 'Growth DUF'), activities=('fab',),
                      related_subbillings=[dict(short='DUFG', long='Growth DUF')],),
                dict(entity=('NEARF', 'Near-field microscopy'), activities=('imag',),
                      related_subbillings=[dict(short='NEARF', long='Near-field microscopy')],),
                dict(entity=('GROWTHIMP', 'Growth and Implantation'), activities=('fab',),
                      related_subbillings=[dict(short='GROWTH', long='Growth'),
                                           dict(short='IMPLANT', long='Ionic Implantation')],),
                dict(entity=('MECA', 'Mechanic Service'), activities=('engi',),
                     related_subbillings=[dict(short='MECA', long='Mechanic Service')], ),
                dict(entity=('ELEC', 'Electronic Service'), activities=('engi',),
                     related_subbillings=[dict(short='ELEC', long='Electronic Service')], ),
                ]

def get_activities_from_entity(entity):
    if entity == '':
        return list(ACTIVITIES.keys())
    else:
        billings = [d['entity'][0] for d in BILLINGS]
        ind = billings.index(entity)
        return BILLINGS[ind]['activities']

def get_entity_long(entity):
    billings = [d['entity'][0] for d in BILLINGS]
    ind = billings.index(entity)
    return BILLINGS[ind]['entity'][1]

def get_subbillings_from_entity_short(entity):
    billings = [d['entity'][0] for d in BILLINGS]
    ind = billings.index(entity)
    return [d['short'] for d in BILLINGS[ind]['related_subbillings']]

def get_subbillings_from_entity_long(entity):
    billings = [d['entity'][0] for d in BILLINGS]
    ind = billings.index(entity)
    return [d['long'] for d in BILLINGS[ind]['related_subbillings']]

def get_billings_from_activity(activity):
    billings = []
    for bill in BILLINGS:
        if activity in bill['activities']:
            billings.append(activity)

def get_billing_entities_as_list():
    return [bill['entity'] for bill in BILLINGS]