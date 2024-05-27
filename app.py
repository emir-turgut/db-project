from flask import Flask, render_template, request, redirect, url_for
from sql import distinct_country_name, set_selected_country, distinct_location_name, get_country_id, \
    set_selected_location, get_location_id, get_selected_country, query_location_data, get_selected_location

app = Flask(__name__)


#initial startup makes it so that distinct countries are listed from the beginning
@app.route('/')
def index():
    countries = distinct_country_name()
    return render_template('index.html', countries=countries, locations=[])


#for the selection of the country
@app.route('/select')
def select_country():
    selected_country = request.args.get('country')
    set_selected_country(selected_country)
    country_ids = get_country_id([selected_country])
    location_names = distinct_location_name(country_ids)
    countries = distinct_country_name()
    return render_template('index.html', countries=countries, locations=location_names)


#for the selection of the location
@app.route('/select_location')
def select_location():
    selected_location = request.args.get('location')
    set_selected_location(selected_location)
    selected_country = get_selected_country()
    country_ids = get_country_id([selected_country])
    location_names = distinct_location_name(country_ids)
    countries = distinct_country_name()
    return render_template('index.html', countries=countries, locations=location_names)


#routes to final query page
@app.route('/query_location', methods=['POST'])
def query_location_route():
    location_id = get_selected_location()
    result = query_location_data(location_id)
    return render_template('query_result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
