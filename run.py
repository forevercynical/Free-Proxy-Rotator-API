from flask import Flask
from FreeProxyList import FreeProxy

ProxyList = FreeProxy()
app = Flask(__name__)

@app.route("/get_proxy")
def get_proxy():
    return ProxyList.get_next_proxy()

app.run(threaded=True, host="0.0.0.0", port=5000, debug=False)
