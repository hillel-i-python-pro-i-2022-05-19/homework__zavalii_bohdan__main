import sqlite3
from typing import Final

import pandas as pd
import requests
from faker import Faker
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from flask_hw7.settings import ROOT_PATH, DB_PATH

app = Flask(__name__)
DATA_FRAME: Final[pd.DataFrame] = pd.read_csv(f"{ROOT_PATH}/people_data.csv")
fake = Faker()


class Connection:

    def __int__(self):
        self._connection: sqlite3.Connection | None = None

    def __enter__(self):
        self._connection = sqlite3.connect(DB_PATH)
        self._connection.row_factory = sqlite3.Row
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


@app.route('/phones/create')
@use_args({"contactName": fields.Str(required=True),
           "phoneValue": fields.Int(required=True)}, location="query")
def phones_create(args):
    with Connection() as connection:
        with connection:
            connection.execute(
                'INSERT INTO phones (contactName, phoneValue) '
                'VALUES (:contactName, :phoneValue);',
                {
                    'contactName': args['contactName'],
                    'phoneValue': args['phoneValue']
                }
            )
    return f"""User <strong><u>{args['contactName']}</u></strong> 
            has been successfully added :)"""


@app.route('/phones/read')
def phones_read():
    with Connection() as connection:
        phones_table = connection.execute('SELECT * FROM phones;').fetchall()
    return "<br>".join([
        f"{person['phoneID']}: "
        f"{person['contactName']} - {person['phoneValue']}"
        for person in phones_table
    ])


@app.route('/phones/update/<int:phoneID>')
@use_args({"phoneValue": fields.Int(required=True)}, location="query")
def phones_update(args, phoneID):
    with Connection() as connection:
        with connection:
            connection.execute(
                'UPDATE phones '
                'SET phoneValue=:phoneValue '
                'WHERE (phoneID=:phoneID); ',
                {'phoneValue': args['phoneValue'], 'phoneID': phoneID}
            )
    return f"""Phone number for person with phone ID - 
    <strong><u>{phoneID}</u></strong> was updated :)"""


@app.route('/phones/delete/<int:phoneID>')
def phones_delete(phoneID):
    with Connection() as connection:
        with connection:
            connection.execute(
                'DELETE FROM phones WHERE (phoneID=:phoneID);',
                {
                    'phoneID': phoneID
                }
            )
    return f"User with phone ID - <strong><i><u>{phoneID}</u></i></strong> " \
           f"was successfully deleted :("


@app.route('/requirements')
def show_requirements():
    with open(f"{ROOT_PATH}/requirements.txt", "r") as f:
        return f.read(-1)
    # return ROOT_PATH.joinpath('requirements.txt').read_text()


@app.route('/generate-users', defaults={'num_of_users': 100})
@app.route('/generate-users/<int:num_of_users>')
def generate_random_users(num_of_users: int) -> str:
    users_list = [
        f"""<p>{fake.first_name()} {fake.ascii_email().lower()}</p>"""
        for _ in range(num_of_users)]
    return "".join(users_list)


@app.route('/space')
def show_num_of_astros() -> str:
    url = "http://api.open-notify.org/astros.json"
    response_in_json = requests.request("GET", url).json()
    return f"At the moment we have: {response_in_json['number']} active astronauts."


@app.route('/mean')
def read_csv_data():
    DATA_FRAME["Height(Centimeters)"] = round(
        DATA_FRAME[' "Height(Inches)"'] * 2.54, 2)
    DATA_FRAME["Weight(Kilograms)"] = round(
        DATA_FRAME[' "Weight(Pounds)"'] / 2.205, 2)
    return f"""<p>Average height is {round(DATA_FRAME["Height(Centimeters)"].mean(), 2)} cm.</p>
    <p>Average weight is {round(DATA_FRAME["Weight(Kilograms)"].mean(), 2)} kg.</p>"""


if __name__ == '__main__':
    app.run()
