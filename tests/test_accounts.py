#!/usr/bin/env python
import unittest
from random import choice
from string import letters, digits
from credentials import credentials as creds
from recurly.client import Client
from recurly.models import Account, ManagedAccount
from recurly.exceptions import RecurlyNotFoundException, RecurlyException

def randomstring(length):
    return ''.join([choice(letters+digits) for x in range(length)])

class AccountTest(unittest.TestCase):

    def setUp(self):
        self.client = Client(
            creds['subdomain'],
            creds['api_key'],
            creds['private_key'],
        )
        self.account_data = {
            'account_code': randomstring(8),
            'username': randomstring(8),
            'first_name': randomstring(8),
            'last_name': randomstring(8),
            # 'email': randomstring(8) + '@example.com',
            'company_name': randomstring(8),
        }

    def test_accounts(self):
        # make sure it's not there.
        self.assertRaises(
            RecurlyNotFoundException,
            self.client.accounts.get,
            self.account_data['account_code'],
        )

        # create an account
        account = Account(**self.account_data)
        created = self.client.accounts.create(account)
        self.assertTrue(isinstance(created, ManagedAccount))

        # check its attributes
        for k, v in self.account_data.items():
            self.assertEqual(getattr(created, k), v)

        # make sure it can be retrieved
        fetched = self.client.accounts.get(
            self.account_data['account_code'],
        )
        self.assertTrue(isinstance(fetched, ManagedAccount))

        # update it
        dct = {'username': randomstring(8)}
        self.assertTrue(self.client.accounts.update(fetched, dct))

        # delete it
        self.assertTrue(self.client.accounts.delete(fetched))

        # can't delete it again.
        self.assertRaises(RecurlyException,
                          self.client.accounts.delete,
                          fetched)

        # make sure it's gone.
        fetched = self.client.accounts.get(self.account_data['account_code'])
        self.assertTrue(fetched.closed)

if __name__ == '__main__':
    unittest.main()
