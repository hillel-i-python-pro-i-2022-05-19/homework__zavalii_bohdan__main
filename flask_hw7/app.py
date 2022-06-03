import pandas as pd
import requests
from faker import Faker
from flask import Flask
from flask_hw7.settings import ROOT_PATH
from typing import Final


app = Flask(__name__)
DATA_FRAME: Final[pd.DataFrame] = pd.read_csv("flask_hw7/people_data.csv")
fake = Faker()


@app.route('/requirements')
def show_requirements():
    with open("flask_hw7/requirements.txt", "r") as f:
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
        DATA_FRAME[' "Weight(Pounds)"'] * 2.205, 2)
    return f"""<p>Average height is {round(DATA_FRAME["Height(Centimeters)"].mean(), 2)} cm.</p>
    <p>Average weight is {round(DATA_FRAME["Weight(Kilograms)"].mean(), 2)} kg.</p>"""


if __name__ == '__main__':
    app.run()
