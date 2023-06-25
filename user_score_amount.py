import csv

def count_positive_negative():
    count_positive = 0
    count_negative = 0

    with open('user_score.csv', 'r', encoding='cp1251') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['sentiment'] == 'Positive':
                count_positive += 1
            elif row['sentiment'] == 'Negative':
                count_negative += 1

    return [count_positive, count_negative]