from flask import Flask, request
import json
import os

import core
import web

side_len = 8

app = Flask(__name__)

@app.route("/")
def get_game_init():
    header_html = web.get_header(title="Blackbox game")
    table_html = web.get_table(side_len)
    atom_coords = core.coords2json(core.get_atom_coords(side_len))
    html = """
    {header}
    <body>
    <h1>Blackbox</h1>
    <p class='slogan'>The mind-bending puzzle</p>
    <p id='atom_coords'>{atom_coords}</p>
    <p id='feedback'>Start by clicking on the numbers ...</p>
    <p id='debug'>Debugging information here ...</p>
    {table}
    <p id='score'>Score: 0 points</p>
    <button type="button" id='reveal'">Done</button>
    <div id="dialog" title="Feedback" style="display: none;"></div>
    </body>
    </html>
    """.format(header=header_html, atom_coords=atom_coords, table=table_html)
    return html
    
@app.route("/get_feedback", methods = ['POST'])
def get_feedback():
    entry = int(request.form['entry'])
    atom_coords = core.coords_str2coords(request.form['atom_coords_str'])
    output_num = core.exit_ray(side_len, atom_coords, entry)
    return json.dumps(output_num)

@app.route("/get_results", methods = ['POST'])
def get_results():
    atom_coords = set(core.coords_str2coords(request.form['atom_coords_str']))
    flag_coords = set(core.coords_str2coords(request.form['flag_coords_str']))
    correct_coords = atom_coords.intersection(flag_coords)
    incorrect_coords = flag_coords.difference(atom_coords)
    unfound_coords = atom_coords.difference(flag_coords)
    if not incorrect_coords:
        message = "Congratulations - you identified the atoms correctly!"
    elif len(incorrect_coords) == len(atom_coords):
        message = "Oops! You didn't guess any of the atoms correctly."
    else:
        message = "Oops! You didn't guess all of the atoms correctly."
    response = {
        "correct_coords": list(correct_coords),
        "incorrect_coords": list(incorrect_coords),
        "unfound_coords": list(unfound_coords),
        "message": message,
    }
    return json.dumps(response)

if __name__ == "__main__":
    app.debug = False
    port = int(os.environb.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
