from flask import Flask
from tasks import smoke_test

app = Flask(__name__)

@app.route("/status")
def status():
    if smoke_test.delay().get() == "ok":
        return "ok"
    else:
        return "not ok"
