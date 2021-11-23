from flask import Flask, render_template, request, jsonify
import predictPrices as predict

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/getCompanies')
def getCompanies():
    companies = predict.brands
    print(companies)
    companies = sorted(companies)
    response = jsonify({"Companies" : companies})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/getSeats')
def getSeats():
    seats = []
    for seat in predict.seats:
        seats.append(int(seat))
    seats = sorted(seats)
    response = jsonify({"Seats": seats})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/getYear')
def getYear():
    year = []
    for y in predict.year:
        year.append(int(y))
    year = sorted(year)
    response = jsonify({"Year": year})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/predictPrice', methods = ['POST'])
def predictPrice():
    brand = request.form["Company"]
    year = int(request.form["Year"])
    engine = int(request.form["Engine"])
    seats = int(request.form["Seats"])
    
    response = jsonify({"Selling_Price" : predict.predictSalesPrice(brand, year, engine, seats)})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    app.run(debug=True)
