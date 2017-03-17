#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from Konstanten import *
from Kontenrahmen_KMU import Kontenrahmen_KMU as KMU_Konti


# Helper
# Date to String
def dts(date, time=True):
	if time:
		return date.strftime(DATUM_ZEIT_FORMAT)
	else:
		return date.strftime(DATUM_FORMAT)


# String to Date
# [!] Returns now() if date_string is ''.
def std(date_string, time=True):
	if date_string == '' or date_string is None:
		return datetime.datetime.now()
	if time:
		return datetime.datetime.strptime(date_string, DATUM_ZEIT_FORMAT)
	else:
		return datetime.datetime.strptime(date_string, DATUM_FORMAT)


konti = []

# Klassen
class Konto:
	def __init__(self, code, name, typ, gegenkonto_code=''):
		self.code = code
		self.name = name
		self.typ = typ
		self.buchungen = []
		self.gegenkonto = next((konto for konto in konti if konto.code == str(gegenkonto_code)), None)

	def get_saldo(self):
		if self.typ == KONTO_TYP_AKTIV or self.typ == KONTO_TYP_AUFWAND:
			return sum([buchung[0] for buchung in self.buchungen]) - sum([buchung[1] for buchung in self.buchungen])
		elif self.typ == KONTO_TYP_PASSIV or self.typ == KONTO_TYP_ERTRAG:
			return sum([buchung[1] for buchung in self.buchungen]) - sum([buchung[0] for buchung in self.buchungen])

	def soll_eintrag(self, betrag):
		self.buchungen.append((betrag, 0))

	def haben_eintrag(self, betrag):
		self.buchungen.append((0, betrag))

	def __str__(self):
		if self.get_saldo() < 0 and self.gegenkonto is not None:
			return str(self.gegenkonto.code + '_' + self.gegenkonto.name[:23]).ljust(30) + str(self.gegenkonto.get_saldo()).rjust(10)
		return str(self.code + '_' + self.name[:23]).ljust(30) + str(self.get_saldo()).rjust(10, '_')


class Buchung:
	def __init__(self, soll_code, haben_code, betrag, date_string='', text=''):
		self.datum = std(date_string)
		self.text = text
		self.soll_konto = next((konto for konto in konti if konto.code == str(soll_code)), None)
		self.haben_konto = next((konto for konto in konti if konto.code == str(haben_code)), None)
		self.betrag = float(betrag)
		self.soll_konto.soll_eintrag(self.betrag)
		self.haben_konto.haben_eintrag(self.betrag)


class Bilanz:
	def __init__(self, datum=datetime.datetime.now()):
		aktivseite = [konto for konto in konti if konto.typ == KONTO_TYP_AKTIV]
		passivseite = [konto for konto in konti if konto.typ == KONTO_TYP_PASSIV]
		aktiv_summe = 0
		passiv_summe = 0
		print('='*83)
		print('Bilanz vom ' + dts(datum, False))
		print('='*83)
		for i in range(max(len(aktivseite), len(passivseite))):
			if i < len(aktivseite):
				aktiven = aktivseite[i]
				aktiv_summe += aktiven.get_saldo()
			else:
				aktiven = ''
			if i < len(passivseite):
				passiven = passivseite[i]
				passiv_summe += passiven.get_saldo()
			else:
				passiven = '' 
			print(str(aktiven).ljust(40) + ' | ' + str(passiven).rjust(40))
		print('-'*83)
		print(str(aktiv_summe).ljust(40) + ' | ' + str(passiv_summe).rjust(40))
		print('='*83)


def load_konti():
	for top_key in KMU_Konti.keys():
		for kat_key in KMU_Konti[top_key].keys():
			if kat_key.isnumeric():
				if len(kat_key) == 4:
					konti.append(
						Konto(kat_key, KMU_Konti[top_key][kat_key]['name'], KMU_Konti[top_key][kat_key]['typ'])
					)
				else:
					for knt_key in KMU_Konti[top_key][kat_key].keys():
						if knt_key.isnumeric():
							if len(knt_key) == 4:
								konti.append(
									Konto(knt_key, KMU_Konti[top_key][kat_key][knt_key]['name'], KMU_Konti[top_key][kat_key][knt_key]['typ'])
								)
							else:
								for k in KMU_Konti[top_key][kat_key][knt_key].keys():
									if k.isnumeric():
										if len(k) == 4:
											konti.append(
												Konto(k, KMU_Konti[top_key][kat_key][knt_key][k]['name'],
																		KMU_Konti[top_key][kat_key][knt_key][k]['typ'])
											)


load_konti()

# Beispiele
Bilanz()
Buchung(1020, 2800, 1000, date_string='10.03.2017 06:24', text='Kapitaleinlage')
Bilanz()
Buchung(1000, 1020, 100, text='Barbezug')
Bilanz()
Buchung('1510', '2000', 500)
Bilanz()
Buchung(2000, '1020', 200)
Bilanz()
