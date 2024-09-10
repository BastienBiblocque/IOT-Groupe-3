from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/temperature', methods=['POST'])
def receive_temperature():
    data = request.json
    print(f"Received data: {data}")
    return jsonify({"status": "success", "received": data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
