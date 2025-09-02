from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/success-table', methods=['POST'])
def success_table():
    global filename
    if request.method == "POST":
        file = request.files['file']
        try:
            df = pandas.read_csv(file)
            geolocator = Nominatim(user_agent="flask_geocoder_2025", timeout=10)
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
            df["coordinates"] = df["Address"].apply(geocode)
            df['Latitude'] = df['coordinates'].apply(lambda x: x.latitude if x else None)
            df['Longitude'] = df['coordinates'].apply(lambda x: x.longitude if x else None)
            df = df.drop(columns=["coordinates"])
            filename = datetime.datetime.now().strftime("sample_files/%Y-%m-%d-%H-%M-%S-%f.csv")
            df.to_csv(filename, index=None)

            return render_template("index.html", text=df.to_html(), btn='download.html')
        except Exception as e:
            print(e)
            return render_template("index.html", text=str(e))

@app.route("/download-file/")
def download():
    return send_file(filename, download_name='yourfile.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
