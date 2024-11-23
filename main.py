from flask import Flask, request, render_template
import nba_api as nba

# Create a Flask instance
app = Flask(__name__)

# Define a route for the homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    options = ['Europe/Paris', 'Europe/Moscow']
    out = nba.get_todays_games('Europe/Paris')
    selected_option = 'Europe/Paris'
    if request.method == 'POST':
        selected_option = request.form['dropdown']
        out = nba.get_todays_games(selected_option)
    return render_template('index.html', out = out, options=options, selected_option=selected_option)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)