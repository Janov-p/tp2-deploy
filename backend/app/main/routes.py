from flask import jsonify
from . import bp

@bp.route('/hello')
def hello():
    return jsonify({
        'message': 'Hello, World!',
        'status': 'success'
    }) 