from helpers import (
    set_chrome_options, scan_carplate_data)
from flask import Flask, request, abort
import os

URL = "https://www.patentechile.com"
app = Flask(__name__)
chrome_options = set_chrome_options()


@app.route("/", methods=['GET'])
def endpoint():
    if request.method == 'GET':

        return {"message": "CARPLATE SCRAPER UP AND RUNNING"}, 200

    else:
        abort(400)


@app.route('/<plate>', methods=['GET'])
def get_car_data(plate):
    print("PLATE: ", plate)
    if (plate is None
        or plate == ''
        or plate == 'favicon.ico'
            or len(plate) != 6):
        return {}
    data = scan_carplate_data(
        carplate=plate, chrome_options=chrome_options,
        url=URL)
    return data


@app.route('/demo/<plate>', methods=['GET'])
def get_car_data_demo(plate):
    print("PLATE: ", plate)
    print("PLATE: ", plate)
    if (plate is None
        or plate == ''
        or plate == 'favicon.ico'
            or len(plate) != 6):
        return {}
    data = scan_carplate_data(
        carplate=plate, chrome_options=chrome_options,
        url=URL)
    custom_data = {
        "model": data['car_data'].get('modelo', ''),
        "brand": data['car_data'].get('marca', ''),
        "plate": data['car_data'].get('patente', ''),
        "year": data['car_data'].get('año', ''),
        "engine": data['car_data'].get('nmotor', ''),
        "chassis": data['car_data'].get('nchasis', '')
    }
    return custom_data


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
