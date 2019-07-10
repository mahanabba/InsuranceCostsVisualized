import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__ , template_folder= 'templates')


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///db/insurance.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Medical = Base.classes.medical

session = Session(engine)

@app.route('/')
def hello():
    return render_template('index.html')


@app.route("/plots")
def samples():
    stmt = session.query(Medical).statement
    df = pd.read_sql_query(stmt, session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    
    # Format the data to send as json
    age = df["age"].map(str)
    bmi = df["bmi"].map(str)
    charges = df["charges"].map(str)
    grouped = df.groupby('sex').mean()
    maleavg = str(grouped.loc["male", "charges"].round(1))
    femaleavg = str(grouped.loc["female", "charges"].round(1))
    grouped2 = df.groupby('smoker').mean()
    smokeavg = str(grouped2.loc["yes", "charges"].round(1))
    nonsmokeavg = str(grouped2.loc["no", "charges"].round(1))
    df2 = pd.get_dummies(df, columns=["smoker"])
    smokes = df2["smoker_yes"].map(str)
    age = age.values.tolist()
    bmi= bmi.values.tolist()
    charges= charges.values.tolist()
    smokes = smokes.values.tolist()
    data = {'age':age,
    'bmi':bmi,
    'charges':charges,
    'maleavg':maleavg,
    'femaleavg':femaleavg,
    'smokeavg':smokeavg,
    'nonsmokeavg':nonsmokeavg,
    'smokes':smokes}

    # print("test")

    # results = session.query(Medical.age, Medical.bmi, Medical.charges).all()
    
    # l = len(results)
    # print(l)

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug = True)