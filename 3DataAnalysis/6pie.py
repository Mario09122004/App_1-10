import justpy as jp
import pandas

# Leer y preparar los datos
data = pandas.read_csv("Reviews.csv", parse_dates=["Timestamp"])
share = data.groupby(['Course Name'])['Rating'].count()   # Cantidad de ratings por curso

# Definición base del gráfico de pastel
chart_def = """
{
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Distribución de Ratings por Curso'
    },
    tooltip: {
        pointFormat: '<b>{point.percentage:.1f}%</b> ({point.y} ratings)'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '{point.name}: {point.percentage:.1f}%'
            },
            showInLegend: true
        }
    },
    series: [
        {
            name: 'Ratings',
            colorByPoint: true,
            data: []
        }
    ]
}
"""

def app():
    wp = jp.QuasarPage()
    jp.QDiv(a=wp, text="Simple Data Analysis", classes="text-h3 text-center")
    jp.QDiv(a=wp, text="Distribución de ratings por curso en formato Pie Chart", classes="text-body1 text-center")
    
    hc = jp.HighCharts(a=wp, options=chart_def)
    
    # Cargar dinámicamente los datos en la gráfica
    hc.options.series[0].data = [{"name": course, "y": int(count)} for course, count in share.items()]
    
    return wp

jp.justpy(app)
