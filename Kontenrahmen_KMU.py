# Kontenrahmen KMU
kontenrahmen_kmu = {
	'1': {
		'name': 'Aktiven',
		'10': {
			'name': 'Umlaufvermögen',
			'100': {
				'name': 'Flüssige Mittel',
				'1000': {
					'name': 'Kasse'
				},
				'1010': {
					'name': 'Post'
				},
				'1020': {
					'name': 'Bank'
				},
				'1050': {
					'name': 'Kurzfristige Geldanlagen'
				},
				'1060': {
					'name': 'Wertschriften'
				}
			},
			'110': {
				'name': 'Forderungen',
				'1100': {
					'name': 'Debitoren (Forderungen aus Lieferungen und Leistungen)'
				},
				'1109': {
					'name': 'Delkredere (Wertberichtigung Debitoren)'
				},
				'1140': {
					'name': 'Vorschüsse und Darlehen'
				},
				'1170': {
					'name': 'Debitor Vorsteuer (MWST)'
				},
				'1176': {
					'name': 'Debitor VSt (Verrechnungssteuer)'
				}
			},
			'120': {
				'name': 'Vorräte',
				'1200': {
					'name': '(Handels-)Waren'
				},
				'1210': {
					'name': 'Rohmaterial'
				},
				'1260': {
					'name': 'Fertige Erzeugnisse'
				},
				'1270': {
					'name': 'Unfertige Erzeugnisse'
				},
				'1280': {
					'name': 'Nicht fakturierte Dienstleistungen'
				}
			},
			'130': {
				'name': 'Vorräte',
				'13': {
					'name': 'Aktive Rechnungsabgrenzung (Transitorische Aktiven)'
				}
			}
		},'14': {
			'name': 'Anlagevermögen',
			'140': {
				'name': 'Finanzanlagen',
				'1440': {
					'name': 'Aktivdarlehen'
				},
				'1480': {
					'name': 'Beteiligungen'
				}
			},
			'150': {
				'name': 'Finanzanlagen',
				'1500': {
					'name': 'Maschinen, Apparate'
				},
				'1509': {
					'name': 'Wertberichtigung'
				},
				'1510': {
					'name': 'Mobiliar, Einrichtungen'
				},
				'1520': {
					'name': 'Büromaschinen, Informatik, Kommunikation'
				},
				'1530': {
					'name': 'Fahrzeuge'
				},
				'1540': {
					'name': 'Werkzeuge, Geräte'
				}
			},
			'160': {
				'name': 'Immobile Sachanlagen',
				'1600': {
					'name': 'Immobilien (Liegenschaften)'
				},
				'1609': {
					'name': 'Wertberichtigung'
				}
			},
			'170': {
				'name': 'Immaterielle Anlagen',
				'1700': {
					'name': 'Patente, Lizenzen'
				}
			}
		}
	},
	'2': {
		'name': 'Passiven',
		'20': {
			'name': 'Fremdkapital',
			'200': {
				'name': 'Kurzfristiges Fremdkapital',
				'2000': {
					'name': 'Kreditoren (Verbindlichkeiten aus Lieferungen und Leistungen)'
				},
				'2100': {
					'name': 'Bank'
				},
				'2200': {
					'name': 'Kreditore Umsatzsteuer (MWST)'
				},
				'2206': {
					'name': 'Kreditor VSt (Verrechnungssteuer)'
				},
				'2260': {
					'name': 'Dividenden'
				},
				'2270': {
					'name': 'Kreditoren Sozialversicherungen'
				},
				'2300': {
					'name': 'Passive Rechnungsabgrenzung (Transitorische Passiven)'
				},
				'2330': {
					'name': 'Kurzfristige Rückstellungen'
				}
			},
			'240': {
				'name': 'Langfristiges Fremdkapital',
				'2400': {
					'name': 'Bankdarlehen'
				},
				'2430': {
					'name': 'Obligationenanleihen'
				},
				'2450': {
					'name': 'Passivdarlehen'
				},
				'2451': {
					'name': 'Hypotheken'
				},
				'2600': {
					'name': 'Langfristige Rückstellungen'
				}
			}
		},
		'28': {
			'name': 'Eigenkapital',
			# Einzelunternehmung
			'2800': {
				'name': 'Eigenkapital'
			},
			'2850': {
				'name': 'Privat'
			}
			# Aktiengesellschaft
			# '2800': {
			# 	'name': 'Aktienkapital'
			# },
			# '2900': {
			# 	'name': 'Gesetzliche Kapitalreserve'
			# },
			# '2950': {
			# 	'name': 'Gesetzliche Gewinnreserve'
			# },
			# '2960': {
			# 	'name': 'Freiwillige Gewinnreserven'
			# },
			# '2970': {
			# 	'name': 'Gewinnvortrag'
			# }
		}
	}
	# TODO: Erfolgsrechnungskonten
}