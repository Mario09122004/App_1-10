from weebcam import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, SingleIntervalTicker, ColumnDataSource

df["Start_String"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_String"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

p = figure(x_axis_type='datetime', height=300, width=500, title="Motion Graph",
           y_range=(0, 1))

p.yaxis.minor_tick_line_color = None
p.ygrid[0].ticker = SingleIntervalTicker(interval=1)

hover = HoverTool(tooltips=[("Start","@Start_String"), ("End", "@End_String")])
p.add_tools(hover)

q = p.quad(left="Start", right="End", top=1, bottom=0, color="red", source=cds)

output_file("Graph.html")
show(p)
