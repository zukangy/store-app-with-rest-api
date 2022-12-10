import uuid
from flask import Flask, request

from db import stores, items

app = Flask(__name__)


@app.get("/stores")
def get_store():
    return {"stores": list(stores.values())}
