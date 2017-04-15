#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Konstanten import KONTO_TYP_AUFWAND, KONTO_TYP_ERTRAG, \
	KONTO_TYP_PASSIV, KONTO_TYP_AKTIV, KONTO_TYP_BILANZ, KONTO_TYP_ERFOLGSRECHNUNG

# Kontenrahmen TEST
Kontenrahmen_TEST = {
	'1': {
		'name': 'Aktiven',
		'10': {
			'name': 'Umlaufvermögen',
			'100': {
				'name': 'Flüssige Mittel',
				'1000': {
					'name': 'Kasse',
					'typ': KONTO_TYP_AKTIV
				},
				'1020': {
					'name': 'Bank',
					'typ': KONTO_TYP_AKTIV,
					'gegenkonto': '2100'
				}
			},
			'110': {
				'name': 'Forderungen',
				'1100': {
					'name': 'Debitoren (Forderungen aus Lieferungen und Leistungen)',
					'typ': KONTO_TYP_AKTIV
				}
			}
		},
	},
	'2': {
		'name': 'Passiven',
		'20': {
			'name': 'Fremdkapital',
			'200': {
				'name': 'Kurzfristiges Fremdkapital',
				'2000': {
					'name': 'Kreditoren (Verbindlichkeiten aus Lieferungen und Leistungen)',
					'typ': KONTO_TYP_PASSIV
				},
				'2100': {
					'name': 'Bank',
					'typ': KONTO_TYP_PASSIV,
					'gegenkonto': '1020'
				}
			}
		},
		'28': {
			'name': 'Eigenkapital',
			'2800': {
				'name': 'Eigenkapital',
				'typ': KONTO_TYP_PASSIV
			},
			'2970': {
				'name': 'Gewinnvortrag',
				'typ': KONTO_TYP_PASSIV
			}
		}
	},
	'3': {
		'name': 'Betriebsertrag aus Lieferungen und Leistungen',
		'3200': {
			'name': 'Warenertrag (Handelserlös)',
			'typ': KONTO_TYP_ERTRAG
		},
		'3400': {
			'name': 'Dienstleistungsertrag',
			'typ': KONTO_TYP_ERTRAG
		}
	},
	'4': {
		'name': 'Aufwand für Material, Waren und Dienstleistungen',
		'4200': {
			'name': 'Warenaufwand',
			'typ': KONTO_TYP_AUFWAND
		}
	},
	'5': {
		'name': 'Personalaufwand',
		'5000': {
			'name': 'Lohnaufwand',
			'typ': KONTO_TYP_AUFWAND
		}
	},
	'6': {
		'name': 'Übriger Betriebsaufwand sowie Zinsen',
		'6000': {
			'name': 'Raumaufwand/Mietaufwand',
			'typ': KONTO_TYP_AUFWAND
		}
	},
	'9': {
		'name': 'Abschluss',
		'9000': {
			'name': 'Erfolgsrechnung',
			'typ': KONTO_TYP_ERFOLGSRECHNUNG
		},
		'9100': {
			'name': 'Bilanz',
			'typ': KONTO_TYP_BILANZ
		}
	}
}
