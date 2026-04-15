from flask import Flask, jsonify, render_template, request
from asyncua import Client, ua
from datetime import datetime
import time
import asyncio
import threading
from . import app

light_data = []
moisture_data = []
nutrient_data = []

OPC_SERVER_URL = "opc.tcp://100.90.187.71:4840/myopcua/server"

# def poll_server():
#     while True:
#         try:
#             new_val = float(asyncio.run(get_opc_data("Moisture")))
#             if len(light_data) > 4:
#                 light_data = light_data[1:]
#             light_data += [new_val]
#         except:
#             pass
#         time.sleep(1)

async def get_opc_data(node):
    # Connect to the OPC UA Server
    client = Client(url=OPC_SERVER_URL)
    async with client:
        # Example node ID to read
        node = client.get_node(f"ns=2;s={node}")
        value = await node.read_value()
        return value


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

@app.route("/dropdown/")
def dropdown():
    plants = ['Fern', 'Succulent', 'Flower', 'Shrub']
    selected = request.args.get('plant')
    plant_info = {'Flower':'Needs bright light', 'Fern':'Keep moist', 'Succulent':'Low water', 'Shrub':'doesnt need much'}
    return render_template('dropdown.html', plants=plants, selected_plant=selected, plant_info=plant_info)



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


# poop = threading.Thread(target = poll_server, daemon=True)
# poop.start()