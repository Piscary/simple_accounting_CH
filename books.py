import datetime

class Konto:
	def __init__(self, code, name, saldo, aktiv):
		self.code = code
		self.name = name
		self.saldo = saldo
		self.aktiv = aktiv

	def soll(self, betrag):
		if self.aktiv:
			self.saldo = self.saldo + betrag
		else:
			self.saldo = self.saldo - betrag

	def haben(self, betrag):
		if self.aktiv:
			self.saldo = self.saldo - betrag
		else:
			self.saldo = self.saldo + betrag

	def __str__(self):
		return str(self.code + '_' + self.name).ljust(20) + str(self.saldo).rjust(20)


class Buchung:
	def __init__(self, soll, haben, betrag):
		soll.soll(betrag)
		haben.haben(betrag)

class Bilanz:
	def __init__(self):
		aktivseite = [key for key in konti.keys() if key[0] == '1']
		passivseite = [key for key in konti.keys() if key[0] == '2']
		akt_sum = 0
		pas_sum = 0
		print('='*83)
		print('Bilanz vom ' + datetime.datetime.now().strftime('%d.%m.%Y'))
		print('='*83)
		for n in range(max(len(aktivseite), len(passivseite))):
			if n < len(aktivseite):
				akt = konti[aktivseite[n]]
				akt_sum = akt_sum + akt.saldo
			else:
				akt = ''
			if n < len(passivseite):
				pas = konti[passivseite[n]]
				pas_sum = pas_sum + pas.saldo
			else:
				pas = '' 
			print(str(akt).ljust(40) + ' | ' + str(pas).rjust(40))
		print('-'*83)
		print(str(akt_sum).ljust(40) + ' | ' + str(pas_sum).rjust(40))
		print('='*83)

konti = {
	'1000' : Konto('1000', 'Kasse', 0, True),
	'1020' : Konto('1020', 'Bank', 0, True),
	'1510' : Konto('1510', 'Mobilien', 0, True),
	'2000' : Konto('2000', 'Kreditoren', 0, False),
	'2800' : Konto('2800', 'Eigenkapital', 0, False)
}




Bilanz()
Buchung(konti['1020'], konti['2800'], 1000)
Bilanz()
Buchung(konti['1000'], konti['1020'], 100)
Bilanz()
Buchung(konti['1510'], konti['2000'], 500)
Bilanz()
Buchung(konti['2000'], konti['1020'], 200)
Bilanz()