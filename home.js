function onLoad() {
    var url = "http://127.0.0.1:5000/getCompanies";
    $.get(url, function(data, status) {
        if(data) {
            var element = document.getElementById("companies_select");
            console.log("companies");
            var companies = data.Companies;
            for (c in companies) {
                var opt = new Option(companies[c]+"");
                element.append(opt);
            }
        }
    });
    url = "http://127.0.0.1:5000/getYear";
    $.get(url, function(data, status) {
        if(data) {
            var element = document.getElementById("year_select");
            console.log("year");
            var year = data.Year;
            for (y in year) {
                var opt = new Option(year[y]);
                element.append(opt);
            }
        }
    });
    url = "http://127.0.0.1:5000/getSeats";
    $.get(url, function(data, status) {
        if(data) {
            var element = document.getElementById("seats_select");
            console.log("seats");
            var seats = data.Seats;
            for (s in seats) {
                var opt = new Option(seats[s]);
                element.append(opt);
            }
        }
    });
}

function predictPrice() {
    var company = document.getElementById("companies_select").value;
    var year = parseInt(document.getElementById("year_select").value);
    var engine = parseInt(document.getElementById("engine_select").value);
    var seats = parseInt(document.getElementById("seats_select").value);
    var url = "http://127.0.0.1:5000/predictPrice";
    $.post(url, {Company:company, Year:year, Engine:engine, Seats:seats}, function(data, status) {
        if(data) {
            var price = parseFloat(data.Selling_Price);
            price = price.toFixed(2);
            document.getElementById("display_price").innerHTML = price + " Lakhs(Approx.)";
        }
    });
}
window.onload = onLoad();
