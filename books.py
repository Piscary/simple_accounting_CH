#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from Konstanten import *
from Kontenrahmen_TEST import Kontenrahmen_TEST as Kontenrahmen


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
buchungen = []


# Klassen
class Konto:
	def __init__(self, code, name, typ, gegenkonto_code=''):
		self.code = code
		self.name = name
		self.typ = typ
		self.buchungen = []
		self.gegenkonto_code = gegenkonto_code
		konti.append(self)

	def get_gegenkonto(self):
		return next((konto for konto in konti if konto.code == str(self.gegenkonto_code)), None)

	def get_saldo(self):
		soll_summe = sum([buchung[0] for buchung in self.buchungen])
		haben_summe = sum([buchung[1] for buchung in self.buchungen])
		if self.typ == KONTO_TYP_AKTIV or self.typ == KONTO_TYP_AUFWAND:
			return soll_summe - haben_summe
		elif self.typ == KONTO_TYP_PASSIV or self.typ == KONTO_TYP_ERTRAG:
			return haben_summe - soll_summe

	def get_typ(self):
		if self.get_saldo():
			if self.get_saldo() < 0 and self.get_gegenkonto():
				return '-' + self.get_gegenkonto().typ
		return self.typ

	def soll_eintrag(self, betrag):
		self.buchungen.append((betrag, 0))

	def haben_eintrag(self, betrag):
		self.buchungen.append((0, betrag))

	def output(self):
		return str(self.code + '_' + self.name[:23]).ljust(30) + str(self.get_saldo()).rjust(10, '_')

	def save_string(self):
		return str(self.code) + ';' + str(self.name) + ';' + str(self.get_saldo())


class Buchung:
	def __init__(self, soll_code, haben_code, betrag, date_string='', text=''):
		self.datum = std(date_string)
		self.text = text
		self.soll_konto = next((konto for konto in konti if konto.code == str(soll_code)), None)
		self.haben_konto = next((konto for konto in konti if konto.code == str(haben_code)), None)
		self.betrag = float(betrag)
		self.soll_konto.soll_eintrag(self.betrag)
		self.haben_konto.haben_eintrag(self.betrag)
		if self.soll_konto.get_gegenkonto():
			self.soll_konto.get_gegenkonto().soll_eintrag(self.betrag)
		if self.haben_konto.get_gegenkonto():
			self.haben_konto.get_gegenkonto().haben_eintrag(self.betrag)
		buchungen.append(self)

	def save_string(self):
		return '{0};{1};{2};{3};{4}'.format(dts(self.datum), self.soll_konto.code, self.haben_konto.code, self.betrag, self.text)


class Bilanz:
	def __init__(self, datum=datetime.datetime.now()):
		self.datum = datum
		self.aktivseite = [konto for konto in konti if konto.get_typ() == KONTO_TYP_AKTIV]
		self.passivseite = [konto for konto in konti if konto.get_typ() == KONTO_TYP_PASSIV]

	def output(self):
		output = ''
		aktiv_summe = 0
		passiv_summe = 0
		output += ('='*83) + '\n'
		output += ('Bilanz vom ' + dts(self.datum, False)) + '\n'
		output += ('='*83) + '\n'
		for i in range(max(len(self.aktivseite), len(self.passivseite))):
			aktiven_str = ' '*40
			passiven_str = ' '*40
			if i < len(self.aktivseite):
				aktiven = self.aktivseite[i]
				aktiv_summe += aktiven.get_saldo()
				aktiven_str = str(aktiven.code + '_' + aktiven.name[:23]).ljust(30) + str(aktiven.get_saldo()).rjust(10, '_')
			if i < len(self.passivseite):
				passiven = self.passivseite[i]
				passiv_summe += passiven.get_saldo()
				passiven_str = str(passiven.code + '_' + passiven.name[:23]).ljust(30) + str(passiven.get_saldo()).rjust(10, '_')
			output += (aktiven_str + ' | ' + passiven_str) + '\n'
		output += ('-'*83) + '\n'
		output += (str(aktiv_summe).ljust(40) + ' | ' + str(passiv_summe).rjust(40)) + '\n'
		output += ('='*83) + '\n'
		return output


class Erfolgsrechnung:
	def __init__(self):
		self.aufwandseite = [konto for konto in konti if konto.get_typ() == KONTO_TYP_AUFWAND]
		self.ertragseite = [konto for konto in konti if konto.get_typ() == KONTO_TYP_ERTRAG]

	def update_gewinnvortrag(self):
		aufwand = sum((konto.get_saldo() for konto in self.aufwandseite))
		ertrag = sum((konto.get_saldo() for konto in self.ertragseite))
		erfolg = ertrag - aufwand
		gewinnvortrag = next((konto for konto in konti if konto.code == '2970'), None)
		gewinnvortrag.history = []
		if erfolg > 0:
			gewinnvortrag.haben_eintrag(erfolg)
		else:
			gewinnvortrag.soll_eintrag(erfolg)

	def output(self):
		# TODO: Erfolgsrechnung verstehen, dann output planen :P
		output = ''
		aufwand_summe = 0
		ertrag_summe = 0
		output += ('='*83) + '\n'
		output += ('Erfolgsrechnung') + '\n'
		output += ('='*83) + '\n'
		for i in range(max(len(self.aufwandseite), len(self.ertragseite))):
			aufwaendungen_str = ' '*40
			ertraege_str = ' '*40
			if i < len(self.aufwandseite):
				aufwaendungen = self.aufwandseite[i]
				aufwand_summe += aufwaendungen.get_saldo()
				aufwaendungen_str = str(aufwaendungen.code + '_' + aufwaendungen.name[:23]).ljust(30) + str(aufwaendungen.get_saldo()).rjust(10, '_')
			if i < len(self.ertragseite):
				ertraege = self.ertragseite[i]
				ertrag_summe += ertraege.get_saldo()
				ertraege_str = str(ertraege.code + '_' + ertraege.name[:23]).ljust(30) + str(ertraege.get_saldo()).rjust(10, '_')
			output += (aufwaendungen_str + ' | ' + ertraege_str) + '\n'
		output += ('-'*83) + '\n'
		output += (str(aufwand_summe).ljust(40) + ' | ' + str(ertrag_summe).rjust(40)) + '\n'
		output += ('='*83) + '\n'
		return output


def load_konti():
	for top_key in Kontenrahmen.keys():
		for kat_key in Kontenrahmen[top_key].keys():
			ebene_1 = Kontenrahmen[top_key][kat_key]
			if kat_key.isnumeric():
				if len(kat_key) == 4:
					gegenkonto = ''
					if 'gegenkonto' in ebene_1.keys():
						gegenkonto = ebene_1['gegenkonto']
					Konto(kat_key, ebene_1['name'], ebene_1['typ'], gegenkonto)
				else:
					for knt_key in Kontenrahmen[top_key][kat_key].keys():
						ebene_2 = ebene_1[knt_key]
						if knt_key.isnumeric():
							if len(knt_key) == 4:
								gegenkonto = ''
								if 'gegenkonto' in ebene_2.keys():
									gegenkonto = ebene_2['gegenkonto']
								Konto(knt_key, ebene_2['name'], ebene_2['typ'], gegenkonto)
							else:
								for k in ebene_2.keys():
									ebene_3 = ebene_2[k]
									if k.isnumeric():
										if len(k) == 4:
											gegenkonto = ''
											if 'gegenkonto' in ebene_3.keys():
												gegenkonto = ebene_3['gegenkonto']
											Konto(k, ebene_3['name'], ebene_3['typ'], gegenkonto)


load_konti()

# Beispiele
Buchung(1020, 2800, 1000, date_string='10.03.2017 06:24', text='Kapitaleinlage')
Buchung(1000, 1020, 100, text='Barbezug')
#Buchung('1510', '2000', 500)
Buchung(6000, 1020, 1000)
#Buchung(1000, 3200, 2500)

ef = Erfolgsrechnung()
ef.update_gewinnvortrag()
print(ef.output())
print(Bilanz().output())


with open('data/TEST_Konten.csv', 'w') as konten_file:
	for konto in konti:
		konten_file.write(konto.save_string() + '\n')
with open('data/TEST_Buchungen.csv', 'w') as buchungen_file:
	for buchung in buchungen:
		buchungen_file.write(buchung.save_string() + '\n')