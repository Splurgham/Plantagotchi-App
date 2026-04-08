from flask import Flask
from flask import render_template, request
from flask import jsonify
from asyncua import Client
from datetime import datetime
from . import app

@app.route("/read")
# async def read_node():
#     async with Client(url="opc.tcp://100.90.187.71:4840/myopcua/server") as client:
#         node = client.get_node("ns=2;s='Water'")
#         value = await node.read_value()
def read():
    var = 5
    return render_template('read.html', var=var)



@app.route('/chart/')
def chart():
    labels = ['January', 'February', 'March', 'April', 'May', 'June']
    data = [0, 10, 15, 8, 22, 5]
    return render_template('chart.html', labels=labels, data=data)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/dropdown/", methods = ['GET'])
def dropdown():
    plants = ['Fern', 'Succulent', 'Flower', 'Shrub']
    return render_template('dropdown.html', plants=plants)



# @app.route("/hello/")
# @app.route("/hello/<name>")
# def hello_there(name = None):
#     return render_template(
#         "hello_there.html",
#         name=name,
#         date=datetime.now()
#     )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

