# Run this example easily with "nitro run URL".
# Get the nitro CLI: https://nitro.h2o.ai/cli/
#
# Like Nitro? Please star us on Github: https://github.com/h2oai/nitro
#
# ===
# About: How to use Bokeh in Nitro apps
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro-bokeh/examples
# Keywords: [visualization]
#
# Setup:
# FILE requirements.txt EOF
# bokeh
# numpy
# pandas
# Flask>=2
# simple-websocket>=0.5
# h2o-nitro[web]
# h2o-nitro-bokeh>=0.1
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP bokeh_basic.py
# ENV FLASK_ENV development
# START python -m flask run
# ===
import numpy as np
import pandas as pd
import simple_websocket
from bokeh.models import HoverTool
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.sampledata.penguins import data
from bokeh.transform import factor_cmap, factor_mark
from flask import Flask, request, send_from_directory

# ----- Nitro app -----

from h2o_nitro import View
from h2o_nitro_web import web_directory
from h2o_nitro_bokeh import bokeh_plugin, bokeh_box


# Entry point
def main(view: View):
    # Show plots one by one.
    view(bokeh_box(make_bokeh_scatterplot()))
    view(bokeh_box(make_bokeh_hexbin_plot()))
    view(bokeh_box(make_bokeh_stacked_area()))


# Nitro instance
nitro = View(
    main,
    title='Nitro + Bokeh',
    caption='A minimal example',
    plugins=[bokeh_plugin()],  # Include the Bokeh plugin
)


# ----- Bokeh plotting routines -----

# Source: http://docs.bokeh.org/en/latest/docs/gallery/marker_map.html
def make_bokeh_scatterplot():
    SPECIES = sorted(data.species.unique())
    MARKERS = ['hex', 'circle_x', 'triangle']

    p = figure(title="Penguin size", background_fill_color="#fafafa")
    p.xaxis.axis_label = 'Flipper Length (mm)'
    p.yaxis.axis_label = 'Body Mass (g)'

    p.scatter("flipper_length_mm", "body_mass_g", source=data,
              legend_group="species", fill_alpha=0.4, size=12,
              marker=factor_mark('species', MARKERS, SPECIES),
              color=factor_cmap('species', 'Category10_3', SPECIES))

    p.legend.location = "top_left"
    p.legend.title = "Species"

    return p


# Source: http://docs.bokeh.org/en/latest/docs/gallery/hexbin.html
def make_bokeh_hexbin_plot():
    n = 500

    x = 2 + 2 * np.random.standard_normal(n)
    y = 2 + 2 * np.random.standard_normal(n)

    p = figure(title="Hexbin for 500 points", match_aspect=True,
               tools="wheel_zoom,reset", background_fill_color='#440154')
    p.grid.visible = False

    r, bins = p.hexbin(x, y, size=0.5, hover_color="pink", hover_alpha=0.8)

    p.circle(x, y, color="white", size=1)

    p.add_tools(HoverTool(
        tooltips=[("count", "@c"), ("(q,r)", "(@q, @r)")],
        mode="mouse", point_policy="follow_mouse", renderers=[r]
    ))

    return p


# Source: http://docs.bokeh.org/en/latest/docs/gallery/stacked_area.html
def make_bokeh_stacked_area():
    n = 10
    df = pd.DataFrame(np.random.randint(10, 100, size=(15, n))).add_prefix('y')

    p = figure(x_range=(0, len(df) - 1), y_range=(0, 800))
    p.grid.minor_grid_line_color = '#eeeeee'

    names = [f"y{i}" for i in range(n)]
    p.varea_stack(stackers=names, x='index', color=brewer['Spectral'][n], legend_label=names, source=df)

    p.legend.orientation = "horizontal"
    p.legend.background_fill_color = "#fafafa"

    return p


# ----- Flask boilerplate -----

app = Flask(__name__, static_folder=web_directory, static_url_path='')


@app.route('/')
def home_page():
    return send_from_directory(web_directory, 'index.html')


@app.route('/nitro', websocket=True)
def socket():
    ws = simple_websocket.Server(request.environ)
    try:
        nitro.serve(ws.send, ws.receive)
    except simple_websocket.ConnectionClosed:
        pass
    return ''


if __name__ == '__main__':
    app.run()
