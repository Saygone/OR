from flask import Flask, request, render_template
import requests
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('first.html')

@app.route('/', methods=['POST'])
def result():
    text = request.form['input_text']
    response = requests.post('http://127.0.0.1:5000/analyze', json={'text': text})
    result = str(response.text)
    prediction = float(result)
    sentiment = "Негативный" if prediction > 0.5 else "Позитивный"
    full = f"Рейтинг данного текста составляет: {prediction} это означает что текст {sentiment}"
    return render_template('first.html', result=full)

@app.route('/data', methods=['GET'])
def data():
    user_dynamic_response = requests.get('http://127.0.0.1:5000/send-data-a')
    user_amount_response = requests.get('http://127.0.0.1:5000/send-data-b')
    kp_month_response = requests.get('http://127.0.0.1:5000/send-data-c')
    kp_week_response = requests.get('http://127.0.0.1:5000/send-data-d')

    user_dynamic_image_data = base64.b64encode(user_dynamic_response.content).decode('utf-8')
    user_amount_image_data = base64.b64encode(user_amount_response.content).decode('utf-8')
    kp_month_image_data = base64.b64encode(kp_month_response.content).decode('utf-8')
    kp_week_image_data = base64.b64encode(kp_week_response.content).decode('utf-8')

    return render_template('second.html',
                           user_dynamic=user_dynamic_image_data,
                           user_amount=user_amount_image_data,
                           kp_month=kp_month_image_data,
                           kp_week=kp_week_image_data)

@app.route('/about', methods=['GET'])
def about():
    return render_template('third.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)