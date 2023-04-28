from flask import Flask, render_template, jsonify
from telegram_handler import mensagens

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mensagens')
def obter_mensagens():
    return jsonify(mensagens)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
