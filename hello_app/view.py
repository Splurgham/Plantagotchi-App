from flask import Flask, jsonify, render_template, request, session
from asyncua import Client, ua
from datetime import datetime
import time
import asyncio
from . import app

light_data = []
moisture_data = []
nitrogen_data = []
phosphorus_data = []
potassium_data = []

OPC_SERVER_URL = "opc.tcp://100.90.187.71:4840/myopcua/server"


async def get_opc_data(node):
    # Connect to the OPC UA Server
    client = Client(url=OPC_SERVER_URL)
    async with client:
        # Example node ID to read
        node = client.get_node(f"ns=2;s={node}")
        value = await node.read_value()
        return value

# async def write_opc_data(data):
#     client = Client(url=OPC_SERVER_URL)
#     async with client:
#         # Example node ID to read
#         node = ("ns=2;s="")
#         await node.write_value(ua.Variant(data, ua.VariantType.Boolean))

def PlantModelHelper(Plant):
    if Plant != None:
        PlantModel(Plant)
        return "Plant model chosen."
    else: 
        return "Please select a plant model."
    
def PlantModel(Plant):
    # Here is where all of the plant model data will be created for each plant type.
    # Then, it will be shipped off to the write_opc_data function, which should parse it
    # and send the model data to the correct nodes on the server.
    return

@app.route("/read")
def read():
    var = asyncio.run(get_opc_data("Moisture"))
    return render_template('read.html', var=var)

@app.route('/chart/')
def chart():

    labels = ['t1','t2','t3','t4','t5']
    global light_data
    new_val1 = float(asyncio.run(get_opc_data("LightIntensity")))
    if len(light_data) > 4:
        light_data = light_data[1:]
    light_data += [new_val1]
    

    labels2 = ['t1','t2','t3','t4','t5']
    global moisture_data
    new_val2 = float(asyncio.run(get_opc_data("Moisture")))
    if len(moisture_data) > 4:
        moisture_data = moisture_data[1:]
    moisture_data += [new_val2]
    

    labels3 = ['Fern', 'bush', 'herb', 'grass', 'flower', 'shrub']
    data3 = [0, 5, 5, 20, 15, 10]
    return render_template('chart.html', labels=labels, data=light_data, labels2=labels2, data2=moisture_data, labels3=labels3, data3=data3)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/dropdown/", methods = ['GET', 'POST'])
def dropdown():
    plants = ['Fern', 'Succulent', 'Flower', 'Shrub']
    selected = request.form.get('plant')
    print(PlantModelHelper(selected))
    plant_info = {'Flower':'Needs bright light.', 'Fern':'Keep moist.', 'Succulent':'Low water.', 'Shrub':"Doesn't need much!"}
    return render_template('dropdown.html', plants=plants, selected_plant=selected, plant_info=plant_info)


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
