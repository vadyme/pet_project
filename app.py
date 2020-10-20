from flask import Flask, render_template, request
import standing_table
import fixture, matchday

app = Flask(__name__)

json_file = './models/standing_table.json'
fixtures_json = './models/fixtures_by_league.json'

# league_id = 2833


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    # return standing_table.build_table(league_id)


@app.route('/standings-table/<int:league_id>', methods=['GET'])
def standings_table(league_id):
    return standing_table.build_table(league_id)


@app.route('/fixtures/<int:league_id>')
def fixtures(league_id):
    return fixture.build_table(league_id)


@app.route('/current/<int:league_id>')
def current(league_id):
    return matchday.build_table(league_id)


if __name__ == "__main__":
    app.run(debug=True)
