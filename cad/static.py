"""
Queste sono tutte le configurazioni di dati di default per il sistema.
"""

EVENT_EMS_STATUS = [
    {
        'long_name': 'UNMANAGED',
        'order': 1
    },
    {
        'long_name': 'ISMANAGING',
        'order': 2
    },
    {
        'long_name': 'MANAGED',
        'order': 3
    },
    {
        'long_name': 'CLOSED',
        'order': 4
    },
]

EVENT_EMS_PLACE = [
    {
        'long_name': 'Casa',
        'short_name': 'K',
        'order': 1
    },
    {
        'long_name': 'Strada',
        'short_name': 'S',
        'order': 2
    },
    {
        'long_name': 'Lavoro',
        'short_name': 'L',
        'order': 3
    },
    {
        'long_name': 'Scuola',
        'short_name': 'Q',
        'order': 4
    },
    {
        'long_name': 'Impianto Sportivo',
        'short_name': 'Y',
        'order': 5
    },
    {
        'long_name': 'Luogo Pubblico',
        'short_name': 'P',
        'order': 6
    },
    {
        'long_name': 'Altro Luogo',
        'short_name': 'Z',
        'order': 7
    }
]

EVENT_EMS_CODE = [
    {
        'long_name': 'Traumatica',
        'short_name': 'C01',
        'order': 1
    },
    {
        'long_name': 'Cardiocircolatoria',
        'short_name': 'C02',
        'order': 2
    },
    {
        'long_name': 'Respiratoria',
        'short_name': 'C03',
        'order': 3
    },
    {
        'long_name': 'Neurologica',
        'short_name': 'C04',
        'order': 4
    },
    {
        'long_name': 'Psichiatrica',
        'short_name': 'C05',
        'order': 5
    },
    {
        'long_name': 'Neoplastica',
        'short_name': 'C06',
        'order': 6
    },
    {
        'long_name': 'Tossicologica',
        'short_name': 'C07',
        'order': 7
    },
    {
        'long_name': 'Metabolica',
        'short_name': 'C08',
        'order': 8
    },
    {
        'long_name': 'Gastroenterologica',
        'short_name': 'C09',
        'order': 9
    },
    {
        'long_name': 'Urologica',
        'short_name': 'C10',
        'order': 10
    },
    {
        'long_name': 'Oculistica',
        'short_name': 'C11',
        'order': 11
    },
    {
        'long_name': 'Otorinolaringoiatrica',
        'short_name': 'C12',
        'order': 12
    },
    {
        'long_name': 'Dermatologica',
        'short_name': 'C13',
        'order': 13
    },
    {
        'long_name': 'Ostetrico-ginecologica',
        'short_name': 'C14',
        'order': 14
    },
    {
        'long_name': 'Infettiva',
        'short_name': 'C15',
        'order': 15
    },
    {
        'long_name': 'Altra Patologia',
        'short_name': 'C19',
        'order': 19
    },
    {
        'long_name': 'Patologia Sconosciuta',
        'short_name': 'C20',
        'order': 20
    }
]

EVENT_EMS_CRITICITY = [
    {
        'long_name': 'Bianco',
        'short_name': 'B',
        'car_types': [
        ],
        'color': '#ffffff',
        'order': 1
    },
    {
        'long_name': 'Verde',
        'short_name': 'V',
        'car_types': [
        ],
        'color': '#3cb371',
        'order': 2
    },
    {
        'long_name': 'Giallo',
        'short_name': 'G',
        'car_types': [
        ],
        'color': '#ffa500',
        'order': 3
    },
    {
        'long_name': 'Rosso',
        'short_name': 'R',
        'car_types': [
            {
                'profile': 'ALS',
                'amount': 1
            }
        ],
        'color': '#ff6347',
        'order': 4
    }
]

UNIT_EMS_STATUS = [
    {
        'long_name': 'OPERATIVE',
        'short_name': 'OPERATIVE',
        'order': 1
    },
    {
        'long_name': 'IN USE',
        'short_name': 'IN USE',
        'order': 2
    },
    {
        'long_name': 'NOT OPERATIVE',
        'short_name': 'NOT OPERATIVE',
        'order': 3
    }
]

UNIT_EMS_PROFILE = [
    {
        'long_name': 'BLSD',
        'short_name': 'BLSD',
        'order': 1
    },
    {
        'long_name': 'ILS',
        'short_name': 'ILS',
        'order': 2
    },
    {
        'long_name': 'ALS',
        'short_name': 'ALS',
        'order': 3
    }
]

UNIT_EMS_TYPE = [
    {
        'long_name': 'AMBULANZA',
        'short_name': 'AMB',
        'order': 1
    },
    {
        'long_name': 'AUTOMEDICA',
        'short_name': 'AUTOM',
        'order': 2
    },
    {
        'long_name': 'ELICOTTERO',
        'short_name': 'ELI',
        'order': 3
    }
]

INTERVENTION_EMS_STATUS = [
    {
        'long_name': 'DISPATCHED',
        'short_name': 'IN',
        'order': 1
    },
    {
        'long_name': 'ENROUTE',
        'short_name': 'PA',
        'order': 2
    },
    {
        'long_name': 'ONPLACE',
        'short_name': 'AR',
        'order': 3
    },
    {
        'long_name': 'ENROUTE_HOSPITAL',
        'short_name': 'CA',
        'order': 4
    },
    {
        'long_name': 'IN_HOSPITAL',
        'short_name': 'FIN',
        'order': 5
    },
    {
        'long_name': 'CLOSED',
        'short_name': 'CLOSED',
        'order': 6
    }
]

INTERVENTION_EMS_EVAL = [
    {
        'long_name': 'Low Criticity',
        'short_name': 1,
        'order': 1
    },
    {
        'long_name': 'Medium Criticity',
        'short_name': 2,
        'order': 2
    },
    {
        'long_name': 'High Criticity',
        'short_name': 3,
        'order': 3
    },
    {
        'long_name': 'Death',
        'short_name': 4,
        'order': 4
    }
]

INTERVENTION_EMS_OUTCOME = {
    1: {
        'long_name': 'Patient to the hospital',
        'short_name': 'TO_H',
        'order': 1
    },
    2: {
        'long_name': 'On place treatment',
        'short_name': 'ON_PLACE_TR',
        'order': 2
    },
    3: {
        'long_name': 'Abort',
        'short_name': 'ABORT',
        'order': 50
    }
}

LOGS = {
    'EVENT_LOG': [
        {
            'message': 'Event Created',
            'order': 1
        },
        {
            'message': 'Event Status Modified',
            'order': 2
        },
        {
            'message': 'Event Data Modified',
            'order': 3
        },
        {
            'message': 'Event Closed',
            'order': 4
        }
    ],
    'MISSION_LOG': [

    ]
}
