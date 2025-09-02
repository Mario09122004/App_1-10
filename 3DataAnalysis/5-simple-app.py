import justpy as jp
import pandas

# Leer y preparar los datos
data = pandas.read_csv("Reviews.csv", parse_dates=["Timestamp"])
data["Month"] = data["Timestamp"].dt.to_period('M')
month_average_crs = data.groupby(["Month", "Course Name"])['Rating'].mean().unstack()

# Definición base del streamgraph
chart_def = """
{
    chart: {
        type: 'streamgraph',
        marginBottom: 30,
        zooming: {
            type: 'x'
        }
    },
    title: {
        text: 'Average Course Ratings Over Time'
    },
    subtitle: {
        text: 'Data grouped by Month and Course'
    },
    xAxis: {
        type: 'category',
        categories: [],
        crosshair: true,
        labels: {
            align: 'left',
            reserveSpace: false,
            rotation: 270
        },
        lineWidth: 0,
        margin: 20,
        tickWidth: 0
    },
    yAxis: {
        visible: false,
        startOnTick: false,
        endOnTick: false,
        minPadding: 0.1,
        maxPadding: 0.15
    },
    legend: {
        enabled: false
    },
    tooltip: {
        shared: true,
        valueDecimals: 2
    },
    plotOptions: {
        series: {
            label: {
                minFontSize: 8,
                maxFontSize: 14,
                style: {
                    color: 'rgba(255,255,255,0.85)'
                }
            },
            accessibility: {
                exposeAsGroupOnly: true
            }
        }
    },
    series: []
}
"""

def app():
    wp = jp.QuasarPage()
    jp.QDiv(a=wp, text="Simple Data Analysis", classes="text-h3 text-center")
    jp.QDiv(a=wp, text="This is a simple data analysis app with streamgraph visualization.", classes="text-body1 text-center")
    
    hc = jp.HighCharts(a=wp, options=chart_def)
    
    # Eje X = meses
    hc.options.xAxis.categories = [str(x) for x in month_average_crs.index]  # convierte Period a string
    
    # Una serie por curso
    for course in month_average_crs.columns:
        hc.options.series.append({
            "name": course,
            "data": [None if pandas.isna(x) else float(x) for x in month_average_crs[course]]
        })
    
    return wp

jp.justpy(app)
