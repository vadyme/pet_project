from flask import Flask, render_template
import standing_table
import fixture

app = Flask(__name__)

json_file = './models/standing_table.json'
fixtures_json = './models/fixtures_by_league.json'

@app.route('/')
def index():
    return standing_table.build_table(2833)

@app.route('/fixtures')
def fixtures():
    return fixture.build_table(2833)


if __name__ == "__main__":
    app.run(debug=True)
