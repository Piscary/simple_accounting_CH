#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import logging
import json
from bottle import route, run, request, post, response, hook
import requests
from SETTINGS import *


# Logger Configuration
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


# Helper
def dts(date='', time=True):
	# Date to String
	if date == '':
		date = datetime.datetime.now()
	if time:
		return date.strftime(DATE_TIME_FORMAT)
	else:
		return date.strftime(DATE_FORMAT)


def std(date_string='', time=True):
	# String to Date
	# [!] Returns now() if date_string is ''.
	if date_string == '':
		return datetime.datetime.now()
	if time:
		return datetime.datetime.strptime(date_string, DATE_TIME_FORMAT)
	else:
		return datetime.datetime.strptime(date_string, DATE_FORMAT)


def d_dict(raw_date='', time=True):
	dd = dict()
	if isinstance(raw_date, datetime.datetime):
		date = dts(raw_date, time)
	elif isinstance(raw_date, str):
		date = raw_date
	dd[POSTING_ATTRIBUTES['DATE']] = date
	return dd


def get_exchange_rates(base, target, date_string=''):
	if date_string == '':
		date = datetime.datetime.now().strftime('%Y-%m-%d')
	else:
		date = std(date_string).strftime('%Y-%m-%d')
	raw = requests.get('http://api.fixer.io/{}?base={}'.format(date, base))
	if raw.ok:
		rates = json.loads(raw.content)
		rate = rates['rates'][target]
		return rate
	return False


class Controller:
	def __init__(self):
		self.account_data = []
		self.posting_data = []
		self.ACCOUNTS = []

	def register_account(self, account):
		self.ACCOUNTS.append(account)

	def register_posting(self, posting):
		self.posting_data.append(posting)

	def save_accounts(self, accounts_path=FILE_PATHS['ACCOUNTS']):
		with open(accounts_path, 'w') as accounts_file:
			json.dump(self.account_data, accounts_file, indent=4)

	def save_postings(self, postings_path=FILE_PATHS['POSTINGS']):
		with open(postings_path, 'w') as postings_file:
			json.dump(self.posting_data, postings_file, indent=4)

	def load_accounts(self, accounts_path=FILE_PATHS['ACCOUNTS']):
		with open(accounts_path, 'r') as accounts_file:
			self.account_data = json.load(accounts_file)
		if self.account_data:
			for key in self.account_data.keys():
				Account(key, self.account_data[key])

	def load_postings(self, postings_path=FILE_PATHS['POSTINGS']):
		with open(postings_path, 'r') as postings_file:
			postings_data = json.load(postings_file)
		if postings_data:
			for posting in postings_data:
				debit = posting[0]
				credit = posting[1]
				amount = posting[2]
				data = posting[3]
				Posting(debit, credit, amount, data)

	def start(self):
		self.load_accounts()
		self.load_postings()

	def save(self):
		self.save_accounts()
		self.save_postings()

CONTROLLER = Controller()


class Account:
	def __init__(self, code, data):
		self.code = code
		logging.info('creating {}'.format(str(self.code)))
		self.data = {}
		self.sub_accounts = []
		for key in data.keys():
			if isinstance(data[key], dict):
				sub_account = Account(key, data[key])
				self.sub_accounts.append(sub_account)
				logging.info('{}.sub_accounts.append({})'.format(str(self.code), str(sub_account.code)))
			elif key in ACCOUNT_ATTRIBUTES.values():
				self.data[key] = data[key]
				logging.info('{}.{} = "{}"'.format(str(self.code), key, str(self.data[key])))
		logging.info('finished creating {}'.format(str(self.code)))
		self.postings = []
		CONTROLLER.register_account(self)

	def get_type(self):
		if ACCOUNT_ATTRIBUTES['TYPE'] in self.data.keys():
			if self.data[ACCOUNT_ATTRIBUTES['TYPE']] in ACCOUNT_TYPES.values():
				return self.data[ACCOUNT_ATTRIBUTES['TYPE']]

	def get_balance(self):
		balance = 0
		if self.get_type() in ACCOUNT_SIDE['LEFT']:
			debit = self.get_debit_amount()
			credit = self.get_credit_amount()
			balance = debit - credit
		elif self.get_type() in ACCOUNT_SIDE['RIGHT']:
			debit = self.get_debit_amount()
			credit = self.get_credit_amount()
			balance = credit - debit
		elif self.get_type() == ACCOUNT_TYPES['PROFIT_CARRYFORWARD']:
			debit = 0
			credit = 0
			for account in CONTROLLER.ACCOUNTS:
				if account.get_type() == ACCOUNT_TYPES['EXPENSE']:
					debit += account.get_balance()
				if account.get_type() == ACCOUNT_TYPES['INCOME']:
					credit += account.get_balance()
			balance = credit - debit
		elif self.get_type() is None:
			for account in self.sub_accounts:
				balance += account.get_balance()
		else:
			raise TypeError('ACCOUNT_TYPE[{}] not supported'.format(str(self.get_type())))
		return balance

	def get_debit_amount(self):
		return sum([posting[POSTING_ATTRIBUTES['DEBIT']] for posting in self.postings])

	def get_credit_amount(self):
		return sum([posting[POSTING_ATTRIBUTES['CREDIT']] for posting in self.postings])

	def add_posting(self, posting):
		self.postings.append(posting)

	def get_vat(self):
		if ACCOUNT_ATTRIBUTES['VAT'] in self.data.keys():
			return float(self.data[ACCOUNT_ATTRIBUTES['VAT']])
		else:
			return DEFAULTS['VAT']

	def get_currency(self):
		if ACCOUNT_ATTRIBUTES['CURRENCY'] in self.data.keys():
			return self.data['CURRENCY']
		else:
			return DEFAULTS['CURRENCY']


class Posting:
	def __init__(self, debit_code, credit_code, amount, raw_data=d_dict()):
		self.debit_account = next((account for account in CONTROLLER.ACCOUNTS if account.code == str(debit_code)), None)
		if self.debit_account is None:
			raise ValueError('No debit_account with debit_code[{}] found.'.format(str(debit_code)))
		self.credit_account = next((account for account in CONTROLLER.ACCOUNTS if account.code == str(credit_code)), None)
		if self.credit_account is None:
			raise ValueError('No credit_account with credit_code[{}] found.'.format(str(debit_code)))
		self.amount = amount
		if self.debit_account.get_vat() != 0.0 and self.debit_account.get_type() not in NO_VAT_ACCOUNT_TYPES:
			self._split_posting_left()
		elif self.credit_account.get_vat() != 0.0:
			self._split_posting_right()
		self.data = {}
		if POSTING_ATTRIBUTES['DATE'] not in raw_data.keys():
			raw_data.update(d_dict())
		if POSTING_ATTRIBUTES['CURRENCY'] not in raw_data.keys():
			raw_data[POSTING_ATTRIBUTES['CURRENCY']] = DEFAULTS['CURRENCY']
		if POSTING_ATTRIBUTES['TEXT'] not in raw_data.keys():
			raw_data[POSTING_ATTRIBUTES['TEXT']] = ''
		for key in raw_data.keys():
			if key in POSTING_ATTRIBUTES.values():
				self.data[key] = raw_data[key]
		self.debit_account.add_posting(self._get_posting_for_debit())
		self.credit_account.add_posting(self._get_posting_for_credit())
		CONTROLLER.register_posting(self._get_tuple())

	def _net_amount(self, account):
		return (float(self.amount) / (100 + account.get_vat())) * 100

	def _split_posting_left(self):
		amount = self._net_amount(self.debit_account)
		vat = self.amount - float(amount)
		data = {POSTING_ATTRIBUTES['TEXT']: '{}{}'.format(self.debit_account.get_vat(), ACCOUNT_ATTRIBUTES['VAT'])}
		tax_account = next((acc for acc in CONTROLLER.ACCOUNTS if acc.get_type() == ACCOUNT_TYPES['INPUT_TAX']), None)
		if tax_account is None:
			raise ValueError('No account with type {} found.'.format(ACCOUNT_TYPES['INPUT_TAX']))
		Posting(tax_account.code, self.credit_account.code, vat, data)

	def _split_posting_right(self):
		amount = self._net_amount(self.credit_account)
		vat = self.amount - float(amount)
		data = {POSTING_ATTRIBUTES['TEXT']: '{}{}'.format(self.credit_account.get_vat(), ACCOUNT_ATTRIBUTES['VAT'])}
		tax_account = next((acc for acc in CONTROLLER.ACCOUNTS if acc.get_type() == ACCOUNT_TYPES['TURNOVER_TAX']), None)
		if tax_account is None:
			raise ValueError('No account with type {} found.'.format(ACCOUNT_TYPES['TURNOVER_TAX']))
		Posting(self.debit_account.code, tax_account.code, vat, data)

	def _get_posting_for_debit(self):
		posting_currency = self.data[POSTING_ATTRIBUTES['CURRENCY']]
		account_currency = self.debit_account.get_currency()
		if posting_currency == account_currency:
			amount = self.amount
		else:
			exchange_rate = get_exchange_rates(
				posting_currency,
				account_currency,
				self.data[POSTING_ATTRIBUTES['DATE']]
			)
			if exchange_rate:
				amount = self.amount*exchange_rate
			else:
				raise ValueError('Exchange rate not found')
		debit_posting = dict()
		debit_posting[POSTING_ATTRIBUTES['DEBIT']] = amount
		debit_posting[POSTING_ATTRIBUTES['CREDIT']] = 0
		for key in self.data.keys():
			debit_posting[key] = self.data[key]
		return debit_posting

	def _get_posting_for_credit(self):
		posting_currency = self.data[POSTING_ATTRIBUTES['CURRENCY']]
		account_currency = self.credit_account.get_currency()
		if posting_currency == account_currency:
			amount = self.amount
		else:
			exchange_rate = get_exchange_rates(
				posting_currency,
				account_currency,
				self.data[POSTING_ATTRIBUTES['DATE']]
			)
			if exchange_rate:
				amount = self.amount*exchange_rate
			else:
				raise ValueError('Exchange rate[{}{}] not found'.format(posting_currency, account_currency))
		credit_posting = dict()
		credit_posting[POSTING_ATTRIBUTES['DEBIT']] = 0
		credit_posting[POSTING_ATTRIBUTES['CREDIT']] = amount
		for key in self.data.keys():
			credit_posting[key] = self.data[key]
		return credit_posting

	def _get_tuple(self):
		debit = str(self.debit_account.code)
		credit = str(self.credit_account.code)
		amount = self.amount
		data = self.data
		return debit, credit, amount, data


class Api:
	def __init__(self):
		pass

	@staticmethod
	@hook('after_request')
	def enable_cors():
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
		response.headers['Content-Type'] = 'application/json'

	@staticmethod
	@route('/')
	def index():
		return 'API is active.'

	@staticmethod
	@post('/api/new/posting')
	def new_posting():
		try:
			posting_data = json.loads(request.body.getvalue())
			debit = posting_data['debit']
			credit = posting_data['credit']
			amount = posting_data['amount']
			date = ''
			if 'date' in posting_data.keys():
				date = posting_data['date']
			data = d_dict(date)
			if 'text' in posting_data.keys():
				data[POSTING_ATTRIBUTES['TEXT']] = posting_data['text']
			data[POSTING_ATTRIBUTES['CURRENCY']] = DEFAULTS['CURRENCY']
			if 'currency' in posting_data.keys():
				data[POSTING_ATTRIBUTES['CURRENCY']] = posting_data['currency']
		except KeyError:
			return 'Failed'
		try:
			Posting(debit, credit, amount, data)
			return 'OK'
		except ValueError:
			return 'Failed'

	@staticmethod
	@route('/api/get/accounts')
	def get_accounts():
		data = []
		accounts = sorted(CONTROLLER.ACCOUNTS, key=lambda x: str(x.code), reverse=False)
		for account in accounts:
			row = dict()
			row['code'] = account.code
			row['name'] = account.data[ACCOUNT_ATTRIBUTES['NAME']]
			row['balance'] = account.get_balance()
			row['type'] = account.get_type()
			row['currency'] = account.get_currency()
			data.append(row)
		return json.dumps(data)

	@staticmethod
	@route('/api/get/postings')
	def get_postings():
		data = []
		for posting in CONTROLLER.posting_data:
			row = dict()
			row['debit'] = posting[0]
			row['credit'] = posting[1]
			row['amount'] = posting[2]
			row['date'] = posting[3][POSTING_ATTRIBUTES['DATE']]
			row['currency'] = posting[3][POSTING_ATTRIBUTES['CURRENCY']]
			row['text'] = posting[3][POSTING_ATTRIBUTES['TEXT']]
			data.append(row)
		return json.dumps(data)

	@staticmethod
	@route('/api/<account_code>')
	@route('/api/<account_code>/postings')
	def show_account(account_code):
		account = next((acc for acc in CONTROLLER.ACCOUNTS if acc.code == account_code), None)
		return json.dumps(account.postings)

	@staticmethod
	@route('/api/save')
	def save_all():
		CONTROLLER.save()
		return 'OK'


API = Api()
CONTROLLER.start()
run(host='localhost', port=8080)
