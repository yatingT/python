<html>
  <body>
    <h1>Welcome!</h1>

    <p>Enjoy the data.</p>
  </body>
</html>

import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)
df = pd.read_csv("main.csv")

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()
    return html

if __name__ == '__main__':
    app.run(host="0.0.0.0") 