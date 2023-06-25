import csv
import io
import pickle

import keras
import matplotlib.pyplot as plt
from flask import Flask, request, send_file
from keras.utils import pad_sequences
import kinopoisk_month
import kinopoisk_week
import user_score_amount

app = Flask(__name__)
max_review_len = 1000
model = keras.models.load_model('best_model_svert.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json['text']
    tokenized_text = tokenizer.texts_to_sequences([text])
    padded_text = pad_sequences(tokenized_text, maxlen=max_review_len)
    prediction = model.predict(padded_text)[0][0]
    sentiment = "Negative" if prediction > 0.5 else "Positive" if prediction < 0.5 else "Neutral"
    score_round = 1 if prediction > 0.5 else 0 if prediction < 0.5 else 0.5
    text = str(text)
    text = text.replace(",", "")

    with open('user_score.csv', mode='r') as file:
        reader = csv.reader(file)
        count = len(list(reader))

    with open('user_score.csv', mode = 'a', newline="") as file:
        writer = csv.writer(file)
        writer.writerow([count, text, prediction, sentiment, score_round])

    return str(prediction)

@app.route('/send-data-a', methods=['GET'])
def send_data_user_dynamic():
    try:
        ids = []
        scores = []

        with open('user_score.csv', 'r', encoding='cp1251') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row['id']
                score = row['score_round']
                ids.append(id)
                scores.append(score)

        labels_plt = ['Позитив', 'Негатив']

        fig, ax = plt.subplots()
        ax.plot(ids, scores, 'o-')
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_ylabel('Тональность')
        ax.set_yticklabels(labels_plt)

        image_stream1 = io.BytesIO()
        plt.savefig(image_stream1, format='png')
        image_stream1.seek(0)
        plt.close(fig)

        return send_file(image_stream1, mimetype='image/png')

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return error_message


@app.route('/send-data-b', methods=['GET'])
def send_data_user_amount():
    try:
        values = user_score_amount.count_positive_negative()

        light_green = (0.6, 0.8, 0.6)
        light_red = (0.8, 0.6, 0.6)

        fig, ax = plt.subplots()

        bars = ax.bar(range(len(values)), values, width=0.6)

        bars[0].set_color(light_green)
        bars[1].set_color(light_red)

        labels = ['Положительные', 'Негативные']
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels)

        ax.set_yscale('log')

        ax.set_ylim([1, 10 ** 4])

        for bar in bars:
            height = bar.get_height()
            ax.annotate(str(int(height)), xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom')

        ax.yaxis.set_major_formatter(plt.NullFormatter())
        ax.set_yticks([])
        ax.set_yticklabels([])

        image_stream2 = io.BytesIO()
        plt.savefig(image_stream2, format='png')
        image_stream2.seek(0)
        plt.close(fig)

        return send_file(image_stream2, mimetype='image/png')

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return error_message

@app.route('/send-data-c', methods=['GET'])
def send_data_kp_amount_month():
    values = kinopoisk_month.get_kp_reviews_data_month()

    # Определение светлых цветов
    light_green = (0.6, 0.8, 0.6)
    light_red = (0.8, 0.6, 0.6)
    light_gray = (0.8, 0.8, 0.8)

    # Создаем график
    fig, ax = plt.subplots()

    # Построение столбчатой диаграммы с указанием цветов и ширины столбцов
    bars = ax.bar(range(len(values)), values, width=0.6)

    # Назначаем цвета столбцов
    bars[0].set_color(light_green)
    bars[1].set_color(light_red)
    bars[2].set_color(light_gray)

    # Настройка меток на оси X
    labels = ['Положительные', 'Негативные', 'Нейтральные']
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)

    # Использование логарифмической шкалы на оси Y
    ax.set_yscale('log')

    # Установка верхнего предела для оси Y
    ax.set_ylim([1, 10 ** 4])

    # Добавление подписей над столбцами
    for bar in bars:
        height = bar.get_height()
        ax.annotate(str(int(height)), xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')

    # Скрытие значений и засечек на оси Y
    ax.yaxis.set_major_formatter(plt.NullFormatter())
    ax.set_yticks([])

    image_stream3 = io.BytesIO()
    plt.savefig(image_stream3, format='png')
    image_stream3.seek(0)  # Reset stream position to the beginning
    plt.close(fig)

    # Send the byte stream as the response with appropriate content type
    return send_file(image_stream3, mimetype='image/png')


@app.route('/send-data-d', methods=['GET'])
def send_data_kp_amount_week():
    values = kinopoisk_week.get_kp_reviews_data_week()

    # Определение светлых цветов
    light_green = (0.6, 0.8, 0.6)
    light_red = (0.8, 0.6, 0.6)
    light_gray = (0.8, 0.8, 0.8)

    # Создаем график
    fig, ax = plt.subplots()

    # Построение столбчатой диаграммы с указанием цветов и ширины столбцов
    bars = ax.bar(range(len(values)), values, width=0.6)

    # Назначаем цвета столбцов
    bars[0].set_color(light_green)
    bars[1].set_color(light_red)
    bars[2].set_color(light_gray)

    # Настройка меток на оси X
    labels = ['Положительные', 'Негативные', 'Нейтральные']
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)

    # Использование логарифмической шкалы на оси Y
    ax.set_yscale('log')

    # Установка верхнего предела для оси Y
    ax.set_ylim([1, 10 ** 4])

    # Добавление подписей над столбцами
    for bar in bars:
        height = bar.get_height()
        ax.annotate(str(int(height)), xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom')

    # Скрытие значений и засечек на оси Y
    ax.yaxis.set_major_formatter(plt.NullFormatter())
    ax.set_yticks([])

    image_stream4 = io.BytesIO()
    plt.savefig(image_stream4, format='png')
    image_stream4.seek(0)  # Reset stream position to the beginning
    plt.close(fig)

    # Send the byte stream as the response with appropriate content type
    return send_file(image_stream4, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)