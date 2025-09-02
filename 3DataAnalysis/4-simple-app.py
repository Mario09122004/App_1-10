import justpy as jp
import pandas
from datetime import datetime
from pytz import utc

data = pandas.read_csv("Reviews.csv", parse_dates=["Timestamp"])
data["Month"] = data["Timestamp"].dt.strftime('%Y-%m')
month_average_crs = data.groupby(['Month', 'Course Name'])["Rating"].mean(numeric_only=True).unstack()

chart_def = """
{
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Average Rating by Course and Month'
    },
    xAxis: {
        categories: []
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        }
    },
    tooltip: {
        shared: true
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        series: {
            marker: {
                enabled: false
            }
        }
    },
    series: []
}
"""

def app():
    wp = jp.QuasarPage()
    jp.QDiv(a=wp, text="Simple Data Analysis", classes="text-h3 text-center")
    jp.QDiv(a=wp, text="This is a simple data analysis app.", classes="text-body1 text-center")
    
    hc = jp.HighCharts(a=wp, options=chart_def)
    
    hc.options.xAxis.categories = list(month_average_crs.index)
    
    for course in month_average_crs.columns:
        hc.options.series.append({
            "name": course,
            "data": [None if pandas.isna(x) else float(x) for x in month_average_crs[course]]
        })
    
    return wp

jp.justpy(app)
