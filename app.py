import uuid
from flask import Flask, request
from flask_smorest import abort

from db import stores, items

app = Flask(__name__)


# Store endpoints
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")

    for store in stores.values():
        if store['name'] == store_data['name']:
            abort(400, message="Store already exists.")

    store_id = uuid.uuid4().hex
    new_store = {**store_data, 'id': store_id}
    stores[store_id] = new_store
    return new_store


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(400, message="Store not found.")


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        store_name = stores[store_id]['name']
        del stores[store_id]
        return {'Message': f"Store {store_name} has been deleted."}
    except KeyError:
        abort(400, message="Store not found.")


# Items endpoints
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "name" not in item_data
        or "store_id" not in item_data
    ):
        abort(404,
              message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")

    for item in items.values():
        if (
            item["name"] == item_data["name"] and item["store_id"] == item_data["store_id"]
        ):
            abort(400, message="Item already exists in the store")

    if item_data['store_id'] not in stores:
        abort(404, message="Store not found.")

    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item
    return new_item, 201


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {'message': "item has been deleted."}
    except KeyError:
        abort(404, message="Item not found")


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="Item not found.")