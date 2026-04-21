from flask import Flask, request, jsonify
from flask_cors import CORS
from graph_utils import parse_graph
from wl import run_wl, compare_graphs

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        k = int(request.form.get('k', 1))

        file1 = request.files.get('file1')
        file2 = request.files.get('file2')

        if not file1:
            return jsonify({"error": "file1 required"}), 400

        g1 = parse_graph(file1.read().decode())

        if file2:
            g2 = parse_graph(file2.read().decode())
            result = compare_graphs(g1, g2, k)
        else:
            result = run_wl(g1, k)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
