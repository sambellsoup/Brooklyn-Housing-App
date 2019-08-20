# Base plot. Don't mess with this!
import pickle
import pandas as pd
import numpy as np
import json

from bokeh.io import output_file, curdoc
from bokeh.plotting import figure, show, ColumnDataSource, reset_output
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.models import ColorBar, Select, HoverTool, GeoJSONDataSource
from bokeh.palettes import RdYlGn
from bokeh.transform import linear_cmap, log_cmap
from bokeh.models.widgets import Slider, Tabs, Panel
from bokeh.layouts import row, column, gridplot, widgetbox

fig = figure()

f = open("mappingdf.pkl", 'rb')
df = pickle.load(f)
f.close

reset_output()

def display_data(selectedYear):
    yr = selectedYear
    df_yr = df[df['year_of_sale'] == yr]
    df_yr = df_yr[df_yr['sale_price'] >= 100000]
    return df_yr

source = ColumnDataSource(data = display_data(2017))

pal= RdYlGn[6]

mapper = log_cmap(field_name = "sale_price", palette = pal, low=100000, low_color = 'green', high=23000000)


tooltips = [("Price","@sale_price"), ("Address","@address"), ("Neighborhood", "@neighborhood")]
slider = Slider(start=2003, end=2017, step=1, value=2017, title = 'Year')
fig = figure(x_axis_type = 'mercator', y_axis_type = 'mercator', tooltips = tooltips, title = 'Brooklyn Residential Housing Prices, 2017')
fig.add_tile(CARTODBPOSITRON)

fig.circle(x = 'coords_x', y = 'coords_y', line_color = mapper,color=mapper, source=source)

color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0,0))

fig.add_layout(color_bar, 'right')
layout = column(fig, slider)

def update_plot(attr, old, new):
    yr = slider.value
    new_data = display_data(yr)
    source = new_data
    fig.title.text = 'Brooklyn Housing Prices, %d' %yr

# Make a slider object: slider
slider = Slider(title = 'Year',start = 2003, end = 2017, step = 1, value = 2017)
slider.on_change('value', update_plot)
# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(fig, widgetbox(slider))
curdoc().add_root(layout)
curdoc().title='Brooklyn Housing Prices'

#Display plot
show(layout)
