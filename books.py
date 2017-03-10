#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

# Konstanten
DATUM_ZEIT_FORMAT = '%d.%m.%Y %H:%M'
DATUM_FORMAT = '%d.%m.%Y'
KONTO_TYP_AKTIV = 'AKTIV'
KONTO_TYP_PASSIV = 'PASSIV'


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


# Klassen
class Konto:
	def __init__(self, code, name):
		self.code = code
		self.name = name
		self.soll = 0
		self.haben = 0
		if self.code[0] == '1':
			self.typ = KONTO_TYP_AKTIV
		elif self.code[0] == '2':
			self.typ = KONTO_TYP_PASSIV
		else:
			self.typ = None

	def get_saldo(self):
		if self.typ == KONTO_TYP_AKTIV:
			return self.soll - self.haben
		elif self.typ == KONTO_TYP_PASSIV:
			return self.haben - self.soll

	def soll_eintrag(self, betrag):
		self.soll = self.soll + betrag

	def haben_eintrag(self, betrag):
		self.haben = self.haben + betrag

	def __str__(self):
		return str(self.code + '_' + self.name).ljust(20) + str(self.get_saldo()).rjust(20)


class Buchung:
	def __init__(self, soll_code, haben_code, betrag, date_string='', text=''):
		self.datum = std(date_string)
		self.text = text
		soll_konto = next((konto for konto in konti if konto.code == str(soll_code)), None)
		haben_konto = next((konto for konto in konti if konto.code == str(haben_code)), None)
		soll_konto.soll_eintrag(betrag)
		haben_konto.haben_eintrag(betrag)


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

konti = [
	Konto('1000', 'Kasse'),
	Konto('1020', 'Bank'),
	Konto('1510', 'Mobilien'),
	Konto('2000', 'Kreditoren'),
	Konto('2800', 'Eigenkapital')
]

# Beispiele
Bilanz()
Buchung(1020, 2800, 1000, date_string='10.03.2017 06:24', text='Kapitaleinlage')
Bilanz()
Buchung(1000, 1020, 100)
Bilanz()
Buchung(1510, 2000, 500)
Bilanz()
Buchung(2000, 1020, 200)
Bilanz()
