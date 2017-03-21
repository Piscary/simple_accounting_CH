#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Konstanten import KONTO_TYP_AUFWAND, KONTO_TYP_ERTRAG, KONTO_TYP_PASSIV, KONTO_TYP_AKTIV

# Kontenrahmen KMU
Kontenrahmen_KMU = {
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
				'1010': {
					'name': 'Post',
					'typ': KONTO_TYP_AKTIV
				},
				'1020': {
					'name': 'Bank',
					'typ': KONTO_TYP_AKTIV,
					'gegenkonto': '2100'
				},
				'1050': {
					'name': 'Kurzfristige Geldanlagen',
					'typ': KONTO_TYP_AKTIV
				},
				'1060': {
					'name': 'Wertschriften',
					'typ': KONTO_TYP_AKTIV
				}
			},
			'110': {
				'name': 'Forderungen',
				'1100': {
					'name': 'Debitoren (Forderungen aus Lieferungen und Leistungen)',
					'typ': KONTO_TYP_AKTIV
				},
				'1109': {
					'name': 'Delkredere (Wertberichtigung Debitoren)',
					'typ': KONTO_TYP_AKTIV
				},
				'1140': {
					'name': 'Vorschüsse und Darlehen',
					'typ': KONTO_TYP_AKTIV
				},
				'1170': {
					'name': 'Debitor Vorsteuer (MWST)',
					'typ': KONTO_TYP_AKTIV
				},
				'1176': {
					'name': 'Debitor VSt (Verrechnungssteuer)',
					'typ': KONTO_TYP_AKTIV
				}
			},
			'120': {
				'name': 'Vorräte',
				'1200': {
					'name': '(Handels-)Waren',
					'typ': KONTO_TYP_AKTIV
				},
				'1210': {
					'name': 'Rohmaterial',
					'typ': KONTO_TYP_AKTIV
				},
				'1260': {
					'name': 'Fertige Erzeugnisse',
					'typ': KONTO_TYP_AKTIV
				},
				'1270': {
					'name': 'Unfertige Erzeugnisse',
					'typ': KONTO_TYP_AKTIV
				},
				'1280': {
					'name': 'Nicht fakturierte Dienstleistungen',
					'typ': KONTO_TYP_AKTIV
				}
			},
			'130': {
				'name': 'Vorräte',
				'1300': {
					'name': 'Aktive Rechnungsabgrenzung (Transitorische Aktiven)',
					'typ': KONTO_TYP_AKTIV
				}
			}
		},'14': {
			'name': 'Anlagevermögen',
			'140': {
				'name': 'Finanzanlagen',
				'1440': {
					'name': 'Aktivdarlehen',
					'typ': KONTO_TYP_AKTIV
				},
				'1480': {
					'name': 'Beteiligungen',
					'typ': KONTO_TYP_AKTIV
				}
			},
			'150': {
				'name': 'Finanzanlagen',
				'1500': {
					'name': 'Maschinen, Apparate',
					'typ': KONTO_TYP_AKTIV
				},
				'1509': {
					'name': 'Wertberichtigung',
					'typ': KONTO_TYP_AKTIV
				},
				'1510': {
					'name': 'Mobiliar, Einrichtungen',
					'typ': KONTO_TYP_AKTIV
				},
				'1520': {
					'name': 'Büromaschinen, Informatik, Kommunikation',
					'typ': KONTO_TYP_AKTIV
				},
				'1530': {
					'name': 'Fahrzeuge',
					'typ': KONTO_TYP_AKTIV
				},
				'1540': {
					'name': 'Werkzeuge, Geräte',
					'typ': KONTO_TYP_AKTIV
				}
			},
			'160': {
				'name': 'Immobile Sachanlagen',
				'1600': {
					'name': 'Immobilien (Liegenschaften)',
					'typ': KONTO_TYP_AKTIV
				},
				'1609': {
					'name': 'Wertberichtigung',
					'typ': KONTO_TYP_AKTIV
				}
			},
			'170': {
				'name': 'Immaterielle Anlagen',
				'1700': {
					'name': 'Patente, Lizenzen',
					'typ': KONTO_TYP_AKTIV
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
					'name': 'Kreditoren (Verbindlichkeiten aus Lieferungen und Leistungen)',
					'typ': KONTO_TYP_PASSIV
				},
				'2100': {
					'name': 'Bank',
					'typ': KONTO_TYP_PASSIV,
					'gegenkonto': '1020'
				},
				'2200': {
					'name': 'Kreditore Umsatzsteuer (MWST)',
					'typ': KONTO_TYP_PASSIV
				},
				'2206': {
					'name': 'Kreditor VSt (Verrechnungssteuer)',
					'typ': KONTO_TYP_PASSIV
				},
				'2260': {
					'name': 'Dividenden',
					'typ': KONTO_TYP_PASSIV
				},
				'2270': {
					'name': 'Kreditoren Sozialversicherungen',
					'typ': KONTO_TYP_PASSIV
				},
				'2300': {
					'name': 'Passive Rechnungsabgrenzung (Transitorische Passiven)',
					'typ': KONTO_TYP_PASSIV
				},
				'2330': {
					'name': 'Kurzfristige Rückstellungen',
					'typ': KONTO_TYP_PASSIV
				}
			},
			'240': {
				'name': 'Langfristiges Fremdkapital',
				'2400': {
					'name': 'Bankdarlehen',
					'typ': KONTO_TYP_PASSIV
				},
				'2430': {
					'name': 'Obligationenanleihen',
					'typ': KONTO_TYP_PASSIV
				},
				'2450': {
					'name': 'Passivdarlehen',
					'typ': KONTO_TYP_PASSIV
				},
				'2451': {
					'name': 'Hypotheken',
					'typ': KONTO_TYP_PASSIV
				},
				'2600': {
					'name': 'Langfristige Rückstellungen',
					'typ': KONTO_TYP_PASSIV
				}
			}
		},
		'28': {
			'name': 'Eigenkapital',
			# == Einzelunternehmung ==
			'2800': {
				'name': 'Eigenkapital',
				'typ': KONTO_TYP_PASSIV
			},
			'2850': {
				'name': 'Privat',
				'typ': KONTO_TYP_PASSIV
			},
			# == Ende Einzelunternehmung ==

			# == Aktiengesellschaft ==
			# '2800': {
			# 	'name': 'Aktienkapital',
			# 	'typ': KONTO_TYP_PASSIV
			# },
			# '2900': {
			# 	'name': 'Gesetzliche Kapitalreserve',
			# 	'typ': KONTO_TYP_PASSIV
			# },
			# '2950': {
			# 	'name': 'Gesetzliche Gewinnreserve',
			# 	'typ': KONTO_TYP_PASSIV
			# },
			# '2960': {
			# 	'name': 'Freiwillige Gewinnreserven',
			# 	'typ': KONTO_TYP_PASSIV
			# },
			'2970': {
				'name': 'Gewinnvortrag',
				'typ': KONTO_TYP_PASSIV
			}
			# == Ende Aktiengesellschaft ==
		}
	},
	'3': {
		'name': 'Betriebsertrag aus Lieferungen und Leistungen',
		'3000': {
			'name': 'Ertrag aus dem Verkauf von Erzeugnissen (Produktionserlös)',
			'typ': KONTO_TYP_ERTRAG
		},
		'3080': {
			'name': 'Bestandesänderungen an unfertigen und fertigen Erzeugnissen',
			'typ': KONTO_TYP_AUFWAND
		},
		'3200': {
			'name': 'Warenertrag (Handelserlös)',
			'typ': KONTO_TYP_ERTRAG
		},
		'3400': {
			'name': 'Dienstleistungsertrag',
			'typ': KONTO_TYP_ERTRAG
		},
		'3800': {
			'name': 'Debitorenverluste (Verluste aus Forderungen)',
			'typ': KONTO_TYP_AUFWAND
		}
	},
	'4': {
		'name': 'Aufwand für Material, Waren und Dienstleistungen',
		'4000': {
			'name': 'Materialaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'4200': {
			'name': 'Warenaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'4400': {
			'name': 'Aufwand fpr Drittleistungen',
			'typ': KONTO_TYP_AUFWAND
		}
	},
	'5': {
		'name': 'Personalaufwand',
		'5000': {
			'name': 'Lohnaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'5700': {
			'name': 'Sozialversicherungsaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'4400': {
			'name': 'Übriger Personalaufwand',
			'typ': KONTO_TYP_AUFWAND
		}
	},
	'6': {
		'name': 'Übriger Betriebsaufwand sowie Zinsen',
		'6000': {
			'name': 'Raumaufwand/Mietaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'6100': {
			'name': 'Unterhalt und Reparaturen',
			'typ': KONTO_TYP_AUFWAND
		},
		'6300': {
			'name': 'Versicherungsaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'6400': {
			'name': 'Energie- und Entsorgungsaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'6500': {
			'name': 'Verwaltungsaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'6600': {
			'name': 'Werbeaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'6700': {
			'name': 'Sonstiger Betriebsaufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'6800': {
			'name': 'Abschreibungen',
			'typ': KONTO_TYP_AUFWAND
		},
		'6900': {
			'name': 'Zinsaufwand (Finanzaufwand)',
			'typ': KONTO_TYP_AUFWAND
		},
		'6950': {
			'name': 'Zinsertrag (Finanzertrag)',
			'typ': KONTO_TYP_ERTRAG
		}
	},
	'7': {
		'name': 'Betrieblicher Nebenerfolg',
		'740': {
			'name': 'Wertschriften-/Beteiligungserfolg',
			'7400': {
				'name': 'Wertschriftenertrag',
				'typ': KONTO_TYP_ERTRAG
			},
			'7410': {
				'name': 'Wertschriftenaufwand',
				'typ': KONTO_TYP_AUFWAND
			},
			'7450': {
				'name': 'Beteiligungsertrag',
				'typ': KONTO_TYP_ERTRAG
			},
			'7460': {
				'name': 'Beteiligungsaufwand',
				'typ': KONTO_TYP_AUFWAND
			}
		},
		'750': {
			'name': 'Liegenschaftserfolg',
			'7500': {
				'name': 'Liegenschaftsertrag',
				'typ': KONTO_TYP_ERTRAG
			},
			'7510': {
				'name': 'Liegenschaftsaufwand',
				'typ': KONTO_TYP_AUFWAND
			}
		}
	},
	'8': {
		'name': 'Neutraler Erfolg',
		'8000': {
			'name': 'Betriebsfremder Aufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'8100': {
			'name': 'Betriebsfremder Ertrag',
			'typ': KONTO_TYP_ERTRAG
		},
		'8500': {
			'name': 'Ausserordentlicher Aufwand',
			'typ': KONTO_TYP_AUFWAND
		},
		'8600': {
			'name': 'Ausserordentlicher Ertrag',
			'typ': KONTO_TYP_ERTRAG
		},
		'8900': {
			'name': 'Direkte Steuern',
			'typ': KONTO_TYP_AUFWAND
		}
	},
	'9': {
		'name': 'Abschluss',
		'9000': {
			'name': 'Erfolgsrechnung',
			'typ': KONTO_TYP_AUFWAND
		},
		'9100': {
			'name': 'Bilanz',
			'typ': KONTO_TYP_ERTRAG
		}
	}
}
