import datetime
import logging
import os
import tempfile

from api import Zodiac


class ZodiacArgs(object):
    def __init__(self, model_group_hash, transactions=None, attributes=None):
        if not transactions:
            transactions = []

        if not attributes:
            attributes = []

        self.model_group_hash = model_group_hash
        self.transactions = transactions
        self.attributes = attributes



def run():
    # TODO: add the "company" stuff
    username = os.environ.get('ZODIAC_USERNAME')
    password = os.environ.get('ZODIAC_PASSWORD')
    model_group_hash = os.environ.get('ZODIAC_MODEL_GROUP_HASH')

    file_path = '/Users/mcginleyr1/Downloads/00643eab-aedf-40c7-89ad-00e9d203904a%2Fraw_tlog.csv'

    zodiac_args = ZodiacArgs(
        model_group_hash=model_group_hash,
        transactions=[file_path],
    )

    conn = Zodiac(username, password)
    conn.submit_job(zodiac_args)




if __name__ == "__main__":
    run()
