""" server.py """
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)

OPENINGS = []
openings = [
    {'venue':'Cool Art place', 'event_title':"Gnarly Art", 'artist':"Bob the builder", 'date_and_time':"Monday 8:00", 'coor1':40.7403, 'coor2':-73.9897},
    {'venue':'Amazing Art place', 'event_title':"Sweet Art", 'artist':"Sally the sculpter", 'date_and_time':"Tuesday 8:00", 'coor1':40.7503, 'coor2':-73.9897}
  ]

app = Flask(__name__, static_url_path='')
app.debug = True


@app.route('/openings')
def get_openings():
    return(jsonify(result=openings))
    

@app.route('/')
def index(openings=openings):
    print(openings)
    return render_template('index.html', events=openings)


@app.route('/openings/', methods=['POST'])
def opening_create():
    opening = request.get_json()
    opening['id'] = len(OPENINGS)
    OPENINGS.append(opening)
    return _opening_response(opening)


@app.route('/openings/<int:id>')
def opening_read(id):
    opening = _opening_get_or_404(id)
    return _opening_response(opening)


@app.route('/openings/<int:id>', methods=['PUT', 'PATCH'])
def opening_update(id):
    opening = _opening_get_or_404(id)
    updates = request.get_json()
    opening.update(updates)
    return _opening_response(opening)


@app.route('/openings/<int:id>', methods=['DELETE'])
def opening_delete(id):
    opening = _opening_get_or_404(id)
    OPENINGS[id] = None
    return _opening_response(opening)


def _opening_get_or_404(id):
    if not (0 <= id < len(OPENINGS)):
        abort(404)
    opening = OPENINGS[id]
    if opening is None:
        abort(404)
    return opening


def _opening_response(opening):
    return jsonify(**opening)


if __name__ == '__main__':
    app.run(port=8000)
