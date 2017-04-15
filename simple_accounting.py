#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import gc
import logging
from SETTINGS import *
from Kontenrahmen_TEST import Kontenrahmen_TEST as Accounts


# Logger Configuration
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
		'%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


# Helper
# Date to String
def dts(date, time=True):
	if time:
		return date.strftime(DATE_TIME_FORMAT)
	else:
		return date.strftime(DATE_FORMAT)


# String to Date
# [!] Returns now() if date_string is ''.
def std(date_string, time=True):
	if date_string == '' or date_string is None:
		return datetime.datetime.now()
	if time:
		return datetime.datetime.strptime(date_string, DATE_TIME_FORMAT)
	else:
		return datetime.datetime.strptime(date_string, DATE_FORMAT)

# Global Variables
LoadedAccounts = []


class Account:
	def __init__(self, account_tuple):
		LoadedAccounts.append(self)
		self.code = account_tuple[0]
		logging.info('creating {}'.format(str(self.code)))
		self.data = {}
		self.sub_accounts = []
		data_tuple = account_tuple[1]
		for key in data_tuple.keys():
			if isinstance(data_tuple[key], dict):
				sub_account_tuple = (key, data_tuple[key])
				sub_account = Account(sub_account_tuple)
				self.sub_accounts.append(sub_account)
				logging.info('{}.sub_accounts.append({})'.format(str(self.code), str(sub_account.code)))
			elif key in ACCOUNT_ATTRIBUTES.values():
				self.data[key] = data_tuple[key]
				logging.info('{}.{} = "{}"'.format(str(self.code), key, str(self.data[key])))
		logging.info('finished creating {}'.format(str(self.code)))
		self.postings = []

	def get_type(self):
		if ACCOUNT_ATTRIBUTES['TYPE'] in self.data.keys():
			if self.data[ACCOUNT_ATTRIBUTES['TYPE']] in ACCOUNT_TYPES.values():
				return self.data[ACCOUNT_ATTRIBUTES['TYPE']]

	def get_balance(self):
		balance = 0
		debit = self.get_debit_amount()
		credit = self.get_credit_amount()
		if self.get_type() in ACCOUNT_SIDE['LEFT']:
			balance = debit - credit
		elif self.get_type() in ACCOUNT_SIDE['RIGHT']:
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
	def __init__(self, debit_code, credit_code, amount, raw_data={}):
		self.debit_account = next((account for account in LoadedAccounts if account.code == str(debit_code)), None)
		if self.debit_account is None:
			raise ValueError('No debit_account with debit_code[{}] found.'.format(str(debit_code)))
		self.credit_account = next((account for account in LoadedAccounts if account.code == str(credit_code)), None)
		if self.credit_account is None:
			raise ValueError('No credit_account with credit_code[{}] found.'.format(str(debit_code)))
		self.amount = amount
		self.data = {}
		for key in raw_data.keys():
			if key in POSTING_ATTRIBUTES.values():
				self.data[key] = raw_data[key]
		self.debit_account.add_posting(self._get_posting_for_debit())
		self.credit_account.add_posting(self._get_posting_for_credit())

	def _get_posting_for_debit(self):
		debit_posting = dict()
		debit_posting[POSTING_ATTRIBUTES['DEBIT']] = self.amount
		debit_posting[POSTING_ATTRIBUTES['CREDIT']] = 0
		for key in self.data.keys():
			debit_posting[key] = self.data.keys()
		return debit_posting

	def _get_posting_for_credit(self):
		credit_posting = dict()
		credit_posting[POSTING_ATTRIBUTES['DEBIT']] = 0
		credit_posting[POSTING_ATTRIBUTES['CREDIT']] = self.amount
		for key in self.data.keys():
			credit_posting[key] = self.data.keys()
		return credit_posting


for a_konto in Accounts.keys():
	Account((a_konto, Accounts[a_konto]))

Posting(1000, 9100, 99.75)
Posting(9100, 2800, 99.75)

for a in LoadedAccounts:
	print(str(a.code).rjust(5), a.get_balance())
