from flask import Flask, request
import json

import web

app = Flask(__name__)

@app.route("/")
def get_game_init():
    header_html = web.get_header(title="Blackbox game")
    table_html = web.get_table(side_len=8)
    html = """
    {}
    <body>
    <h1>Blackbox</h1>
    <p class='slogan'>The mind-bending puzzle</p>
    {}
    </body>
    </html>
    """.format(header_html, table_html)
    return html
    
@app.route("/get_feedback", methods = ['POST'])
def get_feedback():
    number = request.form['number']
    return json.dumps([number,])

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
