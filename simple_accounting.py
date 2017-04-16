#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import logging
import json
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


def d_dict(date='', time=True):
	dd = dict()
	dd[POSTING_ATTRIBUTES['DATE']] = dts(date, time)
	return dd


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


class Posting:
	def __init__(self, debit_code, credit_code, amount, raw_data=d_dict()):
		self.debit_account = next((account for account in CONTROLLER.ACCOUNTS if account.code == str(debit_code)), None)
		if self.debit_account is None:
			raise ValueError('No debit_account with debit_code[{}] found.'.format(str(debit_code)))
		self.credit_account = next((account for account in CONTROLLER.ACCOUNTS if account.code == str(credit_code)), None)
		if self.credit_account is None:
			raise ValueError('No credit_account with credit_code[{}] found.'.format(str(debit_code)))
		self.amount = amount
		self.data = {}
		if POSTING_ATTRIBUTES['DATE'] not in raw_data.keys():
			raw_data.update(d_dict())
		for key in raw_data.keys():
			if key in POSTING_ATTRIBUTES.values():
				self.data[key] = raw_data[key]
		self.debit_account.add_posting(self._get_posting_for_debit())
		self.credit_account.add_posting(self._get_posting_for_credit())
		CONTROLLER.register_posting(self._get_tuple())

	def _get_posting_for_debit(self):
		debit_posting = dict()
		debit_posting[POSTING_ATTRIBUTES['DEBIT']] = self.amount
		debit_posting[POSTING_ATTRIBUTES['CREDIT']] = 0
		for key in self.data.keys():
			debit_posting[key] = self.data[key]
		return debit_posting

	def _get_posting_for_credit(self):
		credit_posting = dict()
		credit_posting[POSTING_ATTRIBUTES['DEBIT']] = 0
		credit_posting[POSTING_ATTRIBUTES['CREDIT']] = self.amount
		for key in self.data.keys():
			credit_posting[key] = self.data[key]
		return credit_posting

	def _get_tuple(self):
		debit = str(self.debit_account.code)
		credit = str(self.credit_account.code)
		amount = self.amount
		data = self.data
		return debit, credit, amount, data


CONTROLLER.start()

for a in CONTROLLER.ACCOUNTS:
	print(str(a.code).rjust(5), str(a.get_balance()))
