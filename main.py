from flask import Flask, request
import json

import core
import web

side_len = 8

app = Flask(__name__)

@app.route("/")
def get_game_init():
    header_html = web.get_header(title="Blackbox game")
    table_html = web.get_table(side_len)
    coordinates = core.coords2json(core.get_coordinates(side_len))
    html = """
    {header}
    <body>
    <h1>Blackbox</h1>
    <p class='slogan'>The mind-bending puzzle</p>
    <p id='coords'>{coords}</p>
    <p id='feedback'>Start by clicking on the numbers ...</p>
    <p id='debug'>Debugging information here ...</p>
    {table}
    <p id='score'>Score: 0 points</p>
    <button type="button" id='reveal'>Done</button> 
    </body>
    </html>
    """.format(header=header_html, coords=coordinates, table=table_html)
    return html
    
@app.route("/get_feedback", methods = ['POST'])
def get_feedback():
    entry = int(request.form['entry'])
    coordinates = core.coords_str2coords(request.form['coords_str'])
    output_num = core.exit_ray(side_len, coordinates, entry)
    return json.dumps(output_num)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
