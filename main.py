from flask import Flask

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
    {}
    </body>
    </html>
    """.format(header_html, table_html)
    return html

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
