import justpy as jp
import pandas
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import utc

data = pandas.read_csv("Reviews.csv", parse_dates=["Timestamp"])
data["Day"] = data["Timestamp"].dt.date
day_average = data.groupby(['Day']).mean(numeric_only=True)

chart_def = """
     {
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'Atmosphere Temperature by Altitude'
    },
    subtitle: {
        text: 'According to the Standard Atmosphere Model'
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Altitude'
        },
        labels: {
            format: '{value} km'
        },
        accessibility: {
            rangeDescription: 'Range: 0 to 80 km.'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Temperature'
        },
        labels: {
            format: '{value}°'
        },
        accessibility: {
            rangeDescription: 'Range: -90°C to 20°C.'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x} km: {point.y}°C'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Temperature',
        data: [
            [0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
            [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]
        ]

    }]
}
"""

def app():
    wp = jp.QuasarPage()
    jp.QDiv(a=wp, text="Simple Data Analysis", classes="text-h3 text-center")
    jp.QDiv(a=wp, text="This is a simple data analysis app.", classes="text-body1 text-center")
    
    hc = jp.HighCharts(a=wp, options=chart_def)
    hc.options.title.text = "Average Rating by Day"
    
    hc.options.xAxis.categories = list(day_average.index)
    hc.options.series[0].data = list(day_average["Rating"])

    return wp

jp.justpy(app)
