from flask import Flask, render_template, request, jsonify
from math import isfinite

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/app')
def app_page():
    return render_template('app.html')

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    # Simple calculator API (add, sub, mul, div)
    data = request.get_json() or {}
    try:
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        op = data.get('op', 'add')
    except Exception:
        return jsonify({'error': 'Invalid numeric input'}), 400

    try:
        if op == 'add':
            res = a + b
        elif op == 'sub':
            res = a - b
        elif op == 'mul':
            res = a * b
        elif op == 'div':
            res = a / b if b != 0 else None
        else:
            return jsonify({'error': 'Unsupported operation'}), 400

        if res is None or not isfinite(res):
            return jsonify({'error': 'Math error (e.g., division by zero)'}), 400

        return jsonify({'result': res})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/convert-temp', methods=['POST'])
def api_convert_temp():
    # Temperature converter API: expects {"value": number, "from": "C"|"F"|"K", "to": "C"|"F"|"K"}
    data = request.get_json() or {}
    try:
        v = float(data.get('value'))
        frm = data.get('from', 'C').upper()
        to = data.get('to', 'C').upper()
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400

    # convert to Celsius first
    def to_celsius(val, frm):
        if frm == 'C': return val
        if frm == 'F': return (val - 32) * 5.0/9.0
        if frm == 'K': return val - 273.15
        raise ValueError('Unsupported unit')

    def from_celsius(c, to):
        if to == 'C': return c
        if to == 'F': return c * 9.0/5.0 + 32
        if to == 'K': return c + 273.15
        raise ValueError('Unsupported unit')

    try:
        c = to_celsius(v, frm)
        out = from_celsius(c, to)
        return jsonify({'result': out})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
