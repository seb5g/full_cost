import os
import codecs
import csv
from full_cost.utils.ldap import LDAP

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "full_cost.settings")

import django
django.setup()
from lab.models import Project, User, Group, Price, Gestionnaire

gest = [dict(last_name='Trupin', first_name='Mireille', email='mireille.trupin@cemes.fr', groups=['NEO', 'MEM', 'M3', 'I3EM']),
        dict(last_name='Rougale', first_name='Muriel', email='muriel.rougalle@cemes.fr', groups=[]),
        dict(last_name='Melendo', first_name='Rose', email='rose-marie.melendo@cemes.fr', groups=['PPM', 'SINANO']),
        dict(last_name='Vidal', first_name='Clémence', email='clemence.vidal@cemes.fr', groups=['GNS'])]

def populate_gestionnaire():
    for g in gest:
        gg = Gestionnaire(last_name=g['last_name'], first_name=g['first_name'], email=g['email'])
        gg.save()
        print(gg)



def populate_project():
    with codecs.open('./project_pi.csv', 'r', 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            pi_surname = row[1].split(' ')[0]
            try:
                pi = User.objects.get(user_last_name__iexact=pi_surname)
            except:
                pi = User.objects.get(user_last_name='OTHER')
            p = Project(project_name=row[0].upper(), project_pi=pi, pricing=row[2])
            p.save()
            print(row)

def populate_users():
    with codecs.open('./personnel.csv', 'r', 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lgroup = get_group(row[0].upper())
            user = User(user_last_name=row[0].upper(), user_first_name=row[1].capitalize(), group=lgroup)
            user.save()
            print(row)
        user = User(user_last_name='OTHER', user_first_name='Name')
        user.save()

def get_gest_from_group(group):
    for g in gest:
        if group in g['groups']:
            return Gestionnaire.objects.get(last_name__iexact=g['last_name'])


def get_group(user):
    lgroup = None
    ldap = LDAP()
    group = ldap.get_group_ldap_last_name(user)
    if group is not None:
        g = Group.objects.filter(group__iexact=group['short'])
        if not g.exists():
            gest = get_gest_from_group(group['short'])
            lgroup = Group(group=group['short'].upper(), description=group['long'], gestionnaire=gest)
            lgroup.save()
        else:
            lgroup = g[0]
    return lgroup




def populate_groups():
    groups = ['Neo', 'M3', 'GNS', 'I3EM', 'PPM', 'SiNano', 'MEM', 'Service']
    for g in groups:
        if not Group.objects.filter(group__iexact=g).exists():
            u = Group(group=g)
            u.save()
            print(g)




def populate_osp_experiments():
    from osp.models import Experiment, sub_billings

    osp_experiments = [['Xplora', sub_billings[0][0]],
                       ['T64000', sub_billings[0][0]],
                       ['Visible', sub_billings[0][0]],
                       ['UV', sub_billings[0][0]],
                       ['Reflectivité', sub_billings[0][0]],
                       ['TERS', sub_billings[0][0]],
                       ['FLIM', sub_billings[0][0]],
                       ['Plasmonique quantique', sub_billings[0][0]],
                       ['Femto', sub_billings[0][0]],
                       ['UV (A125)', sub_billings[0][0]],
                       ['IR (A125)', sub_billings[0][0]],
                       ['Electrochimie (A125)', sub_billings[0][0]], ]
    for e in osp_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_mphys_experiments():
    from mphys.models import Experiment, sub_billings
    exps = ['ATD/ATG', 'Adsorption Gaz', 'Titrimétrie','DLS', 'Zetamétrie',
    'Granulométrie Laser', 'Réfractométrie', 'Spectrofluorométrie',
    'Sonde Puissance', 'Préparation Echantillon (A121)', 'Pycnométrie',
    'Binoculaire', 'Electrochimie', 'Fours à Moufle', 'Fours tubulaires','Etuves',]

    mphys_experiments = [['PPMS', sub_billings[0][0]],
                       ['RX-D8 Advance', sub_billings[1][0]],
                         ['RX-D8 Discover', sub_billings[1][0]],
                       ['MEB', sub_billings[1][0]],
                       ['Traction', sub_billings[1][0]],
                       ['Fluage', sub_billings[1][0]],]

    for exp in exps:
        mphys_experiments.append([f'Powder-{exp}', sub_billings[1][0]])
    for e in mphys_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_chem_experiments():
    from chem.models import Experiment, sub_billings

    chem_experiments = [['A103', sub_billings[0][0]],
                       ['A105', sub_billings[0][0]],
                       ['A107', sub_billings[0][0]],
                       ['A109', sub_billings[0][0]],
                       ['A115', sub_billings[0][0]],
                       ['A117', sub_billings[0][0]],
                        ['A123', sub_billings[0][0]],
                        ['A127', sub_billings[0][0]],
                        ['P003 MW', sub_billings[0][0]],
                        ['P007 BG', sub_billings[0][0]],
                        ['A121', sub_billings[0][0]],
                        ['A119', sub_billings[0][0]],]

    for e in chem_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_fab_experiments():
    from fab.models import Experiment, sub_billings
    CR_exps = ['Laser lithography', 'Photolithography', 'Physical Vapor Deposition - sputtering',
    'Physical Vapor Deposition - ebeam', 'Plasma etching - RIE', 'Ion beam etching',
    'Chemistry (wet etching, surface treatments)', 'Electrical Characterizations', 'Mechanical profilometer']

    G_exps = ['Growth', 'Four', 'Four RTA']

    fab_experiments = [(f'GI-{exp}', sub_billings[2][0]) for exp in G_exps]
    fab_experiments.append(('GI-Implantation', sub_billings[3][0]))
    fab_experiments.append(('DUF Growth', sub_billings[1][0]))
    fab_experiments.extend([(f'CR-{exp}', sub_billings[0][0]) for exp in CR_exps])

    for e in fab_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_imag_experiments():
    from imag.models import Experiment, sub_billings

    imag_experiments = [['LT-UHV', sub_billings[0][0]],
                       ['DUF RT', sub_billings[0][0]],
                       ['DUF VT', sub_billings[0][0]],
                       ['LT-4tips', sub_billings[1][0]],
                       ['Multimode', sub_billings[2][0]],
                       ['D3000', sub_billings[2][0]],
                        ['D3100-STMLE', sub_billings[2][0]],]

    for e in imag_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def set_prices(prices, entity):
    for p in prices:
        billing = Price(price_category=p[0], price=p[1], price_name=p[2], price_entity=entity)
        billing.save()
        print(billing)

def populate_prices():

    for p in Price.objects.all():
        p.delete()

    ### SPECTRO entity
    entity = 'SPECTRO'
    prices = [ ['T1', 653.22, 'SPEC'],
                ['T3', 276.31, 'SPEC'],
              ['T3ANR', 48.72, 'SPEC'],
              ]
    set_prices(prices, entity)

    ### TEM entity
    entity = 'TEM'
    prices = [['T1', 1399.21, 'META'],
              ['T3', 850.19, 'META'],
              ['T3ANR', 141.12, 'META'],
              ['T1', 500.82, 'METC'],
              ['T3', 291.17, 'METC'],
              ['T3ANR', 147.62, 'METC'],
              ]
    set_prices(prices, entity)

    ### PREPA entity
    entity = 'PREPA'
    prices = [['T1', 369.84, 'PREPC'],
              ['T3', 149.19, 'PREPC'],
              ['T3ANR', 32.20, 'PREPC'],
              ['T1', 881.11, 'FIBp'],
              ['T3', 549.20, 'FIBp'],
              ['T3ANR', 72.03, 'FIBp'],
              ['T1', 221.76, 'SOFT'],
              ['T3', 107.46, 'SOFT'],
              ['T3ANR', 74.84, 'SOFT'],
              ]
    set_prices(prices, entity)

    ### MEBA entity
    entity = 'MEBA'
    prices = [['T1', 877.04, 'MEBA'],
              ['T3', 530.65, 'MEBA'],
              ['T3ANR', 139.11, 'MEBA'],
              ]
    set_prices(prices, entity)

    ### FIB clean Room
    entity = 'FIBCR'
    prices = [['T1', 1376.79, 'FIBc'],
              ['T3', 823.61, 'FIBc'],
              ['T3ANR', 270.54, 'FIBc'],
              ]
    set_prices(prices, entity)

    ### MAGNETIC entity
    entity = 'MAGNETIC'
    prices = [['T1', 688.61, 'MAG'],
              ['T3', 67.35, 'MAG'],
              ['T3ANR', 113.27, 'MAG'],
              ]
    set_prices(prices, entity)

    ### MATCARAC entity
    entity = 'MATCARAC'
    prices = [['T1', 291.26, 'MATC'],
              ['T3', 166.98, 'MATC'],
              ['T3ANR', 27.58, 'MATC'],
              ]
    set_prices(prices, entity)

    ### CHEM entity
    entity = 'CHEM'
    prices = [['T1', 277.86, 'CHEM'],
              ['T3', 81.92, 'CHEM'],
              ['T3ANR', 91.88, 'CHEM'],
              ]
    set_prices(prices, entity)

    ### UHVI entity
    entity = 'UHVI'
    prices = [['T1', 234.0, 'UHVI'],
              ['T3', 81.98, 'UHVI'],
              ['T3ANR', 138.09, 'UHVI'],
              ]
    set_prices(prices, entity)

    ### LT4 entity
    entity = 'LT4'
    prices = [['T1', 2855.80, 'LT4'],
              ['T3', 1713.60, 'LT4'],
              ['T3ANR', 261.54, 'LT4'],
              ]
    set_prices(prices, entity)

    ### NEARF entity
    entity = 'NEARF'
    prices = [['T1', 727.77, 'NEARF'],
              ['T3', 30.35, 'NEARF'],
              ['T3ANR', 93.89, 'NEARF'],
              ]
    set_prices(prices, entity)

    ### CLEANR entity
    entity = 'CLEANR'
    prices = [['T2', 960.61, 'CLEANR'],
              ['T3', 526.94, 'CLEANR'],
              ['T3ANR', 152.84, 'CLEANR'],
              ]
    set_prices(prices, entity)

    ### DUFG entity
    entity = 'DUFG'
    prices = [['T1', 2203.76, 'DUFG'],
              ['T3', 808.94, 'DUFG'],
              ['T3ANR', 1137.65, 'DUFG'],
              ]
    set_prices(prices, entity)

    ### GROWTH entity
    entity = 'GROWTH'
    prices = [['T1', 199.63, 'GROWTH'],
              ['T3', 118.02, 'GROWTH'],
              ['T3ANR', 28.94, 'GROWTH'],
              ]
    set_prices(prices, entity)

    ### IMPLANT entity
    entity = 'IMPLANT'
    prices = [['T1', 441.31, 'IMPLANT'],
              ['T3', 236.71, 'IMPLANT'],
              ['T3ANR', 120.59, 'IMPLANT'],
              ]
    set_prices(prices, entity)

    ### ELEC entity
    entity = 'ELEC'
    prices = [['T1', 1275.23, 'ELEC'],
              ['T3', 774.17, 'ELEC'],
              ['T3ANR', 78.19, 'ELEC'],
              ]
    set_prices(prices, entity)


    ### MECA entity
    entity = 'MECA'
    prices = [['T1', 515.84, 'MECA'],
              ['T3', 294.45, 'MECA'],
              ['T3ANR', 105.14, 'MECA'],
              ]
    set_prices(prices, entity)



def populate_fib_experiments():
    from fib.models import Experiment, sub_billings, fibs

    fib_experiments = [['TEM Preparation', sub_billings[0][0],fibs[0][0]],
                       ['FIB', sub_billings[0][0],fibs[0][0]],
                       ['SEM', sub_billings[1][0],fibs[0][0]],
                       ['EDS', sub_billings[1][0],fibs[0][0]],
                       ['EBSD', sub_billings[1][0],fibs[0][0]],
                       ['SEM', sub_billings[1][0],fibs[1][0]],
                       ['Lithography', sub_billings[1][0],fibs[1][0]],
                       ['FIB', sub_billings[2][0],fibs[1][0]],]

    for e in fib_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1], fib_name=e[2])
        exp.save()
        print(e)

def populate_engi_experiments():
    from engi.models import Experiment, sub_billings
    from lab.models import User
    elec_people = ['pertel', 'Lasfar']
    meca_people = ['Abeilhou', 'Auriol', 'Gatti']

    engi_experiments = [(User.objects.get(user_last_name__iexact=p), sub_billings[1][0],) for p in elec_people]
    engi_experiments.extend([(User.objects.get(user_last_name__iexact=p), sub_billings[0][0], ) for p in meca_people])

    for e in engi_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_prepa_experiments():
    from prepa.models import Experiment, sub_billings

    prep_experiments = [['PIPS', sub_billings[0][0]],
                       ['Tripod', sub_billings[0][0]],
                       ['Electropolishing', sub_billings[0][0]],
                       ['MEB', sub_billings[0][0]],
                       ['Other', sub_billings[0][0]],
                       ['Soft Matter', sub_billings[2][0]],
                       ]

    for e in prep_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_met_experiments():
    from met.models import Experiment, sub_billings

    prep_experiments = [['JEOL', sub_billings[0][0]],
                       ['CM20 FEG', sub_billings[0][0]],
                       ['HF2000', sub_billings[0][0]],
                       ['CM30', sub_billings[0][0]],
                       ['TECNAI', sub_billings[1][0]],
                       ['I2TEM', sub_billings[1][0]],]

    for e in prep_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

if __name__ == '__main__':
    pass
    # populate_fib_experiments()
    # populate_osp_experiments()
    # populate_prepa_experiments()
    # populate_met_experiments()
    # populate_mphys_experiments()
    # populate_fab_experiments()
    #populate_engi_experiments()
    # populate_chem_experiments()
    # populate_imag_experiments()
    # # populate_gestionnaire()
    populate_prices()
    #populate_users()

    #populate_project()


