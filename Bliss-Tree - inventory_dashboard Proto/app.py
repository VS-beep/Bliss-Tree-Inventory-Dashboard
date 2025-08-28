from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "inventory.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    inventory = load_data()
    return render_template("index.html", inventory=inventory)

@app.route("/add", methods=["POST"])
def add_item():
    inventory = load_data()
    item = {
        "name": request.form["name"],
        "quantity": int(request.form["quantity"]),
        "threshold": int(request.form["threshold"])
    }
    inventory.append(item)
    save_data(inventory)
    return redirect(url_for("index"))

@app.route("/update/<int:item_id>", methods=["POST"])
def update_item(item_id):
    inventory = load_data()
    inventory[item_id]["quantity"] = int(request.form["quantity"])
    save_data(inventory)
    return redirect(url_for("index"))

@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    inventory = load_data()
    inventory.pop(item_id)
    save_data(inventory)
    return redirect(url_for("index"))

@app.route("/api/inventory")
def api_inventory():
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(debug=True)
