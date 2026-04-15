from flask import Flask, jsonify, render_template, request
from asyncua import Client, ua
from datetime import datetime
import asyncio
from . import app

# OPC_SERVER_URL = "opc.tcp://"

# async def get_opc_data():
#     # Connect to the OPC UA Server
#     client = Client(url=OPC_SERVER_URL)
#     async with client:
#         # Example node ID to read
#         node = client.get_node("ns=2;s='Water'")
#         value = await node.read_value()
#         return value


# @app.route('/api/opc-data')
# def get_opcdata():
#     # Run async function in synchronous Flask route
#     try:
#         data = asyncio.run(get_opc_data())
#         return jsonify({"node_value": data})
#     except Exception as e:
#         return jsonify({"error": str(e)})


@app.route("/read")
def read():
    var = 5
    return render_template('read.html', var=var)



@app.route('/chart/')
def chart():
    labels = ['January', 'February', 'March', 'April', 'May', 'June']
    data = [0, 10, 15, 8, 22, 5]
    labels2 = ['Fern', 'bush', 'herb', 'grass', 'flower', 'shrub']
    data2 = [0, 10, 15, 20, 20, 20]
    labels3 = ['Fern', 'bush', 'herb', 'grass', 'flower', 'shrub']
    data3 = [0, 5, 5, 20, 15, 10]
    return render_template('chart.html', labels=labels, data=data, labels2=labels2, data2=data2, labels3=labels3, data3=data3)


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

