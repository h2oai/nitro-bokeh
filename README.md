# Bokeh plugin for H2O Nitro

This plugin lets you use [Bokeh](https://docs.bokeh.org/en/latest/) visualizations in [Nitro](https://github.com/h2oai/nitro)
apps.

## Demo

![Demo](demo.gif)

[View source](examples/bokeh_basic.py).

## Install

```
pip install h2o-nitro-bokeh
```

## Usage

1. Import the plugin:

```py 
from h2o_nitro_bokeh import bokeh_plugin, bokeh_box
```

2. Register the plugin:

```py 
nitro = View(main, title='My App', caption='v1.0', plugins=[bokeh_plugin()])
```

3. Use the plugin:

```py 
# Make a plot
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")
p.line(x, y, legend_label="Temp.", line_width=2)

# Display the plot
view(bokeh_box(p))
```

## Change Log

- v0.2.1 - Jun 09, 2022
    - Fixed
        - Don't return value from plots.
- v0.2.0 - May 39, 2022
    - Perf
        - Quicker loading
- v0.1.0 - May 25, 2022
    - Initial Version

