from flask import Flask, request, render_template, jsonify, redirect, url_for
import nba_api as nba

# Create a Flask instance
app = Flask(__name__)

# Define a route for the homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/api/get_schedule', methods=['GET', 'POST'])
def get_schedule():
    data = request.get_json() 
    time_zone:str  = data['timeZone']
    out = nba.get_todays_games(time_zone)
    response = {
         'status': 'OK',
         'games':out   
    }
    return jsonify(response),200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)