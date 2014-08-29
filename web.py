#! /usr/bin/python3.4

"""
Web interface code
"""

import core

def get_header(title):
    return """
    <!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'
    'http://www.w3.org/TR/html4/loose.dtd'>
    <html>
    <head>
    <title>{}</title>
    <link rel="stylesheet" type="text/css"
        media="all" href="http://fonts.googleapis.com/css?family=PT%20Sans" />
    <link rel='stylesheet' type='text/css'
          href='static/css/main.css' />
    <link rel='stylesheet' type='text/css'
          href='static/css/print.css'
          media='print' />
    <script type="text/javascript" src="static/js/jquery.min.js"></script>
    <script type="text/javascript" src="static/js/blackbox.js"></script>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name='description'
        content="Blackbox puzzle game">
    <meta name='keywords'
        content="puzzle, game, blackbox">
    </head>
    """.format(title)

def get_table(side_len):
    """
    Number outer, non-corner cells from bottom left as 1 going around
    anti-clockwise.
    """
    coordinates = core.get_coordinates(side_len)
    # top row
    top_cells = []
    for i in range(3*side_len-1, 2*side_len-1, -1):
        top_cells.append("<td class='outer_default'>{}</td>".format(i+1))
    top_cells_html = "".join(top_cells)
    top_row_html = ("<tr><td class='corner'></td>" + top_cells_html
        + "<td class='corner'></td></tr>")
    # middle
    right_col = range(2*side_len, side_len, -1)
    left_col = range(3*side_len+1, 4*side_len+1)
    colnums = zip(left_col, right_col)
    inside_mid_row = ("<td align=center class='inner_default'>"
        + "</td>")*side_len
    mid_rows = []
    for l_num, r_num in colnums:
        mid_row = ("<tr><td class='outer_default'>{}</td>".format(l_num)
        + inside_mid_row + "<td class='outer_default'>{}</td></tr>".format(r_num))
        mid_rows.append(mid_row)
    mid_rows_html = "\n".join(mid_rows)
    # bottom row
    bottom_cells = []
    for i in range(side_len):
        bottom_cells.append("<td class='outer_default'>{}</td>".format(i+1))
    bottom_cells_html = "".join(bottom_cells)
    bottom_row_html = ("<tr><td class='corner'></td>" + bottom_cells_html
        + "<td class='corner'></td></tr>")
    # assemble
    rows_html = top_row_html + "\n" + mid_rows_html + "\n" + bottom_row_html
    html = """
    <table>
    <tbody>
    {}
    
    </tbody>
    </table>
    """.format(rows_html)
    return html
