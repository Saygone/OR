import requests
import json
from PIL import Image

'''url = "localhost:5000/analyze"

text = "Хороший фильм, смотрел с удовольствием"

payload = {"text": text}
headers = {"content-type": "application/json"}

response = requests.post("http://localhost:5000/analyze", json=payload, headers=headers)
predict = response.json()
print(predict)

prediction = float(predict)
print(1 - prediction)'''

response = requests.post('http://127.0.0.1:5000/data')
plot_data = response.json()['plot']
image = Image.open(io.BytesIO(plot_data))
image.show()