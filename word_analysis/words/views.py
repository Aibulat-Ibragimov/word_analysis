from django.shortcuts import render
from django.http import HttpResponse
import string
import math
from collections import Counter


def process_text(text):
    """
    Обрабатывает текст, приводя его к нижнему регистру, удаляя пунктуацию и
    разделяя на слова.
    """
    text = text.lower()  # Приводим весь текст к нижнему регистру.
    text = text.translate(str.maketrans('', '', string.punctuation))   # Удаляем все знаки пунктуации из текста.
    words = text.split()  # Разделяем текст на отдельные слова и помещаем их в список words.
    return words


def calculate_tf_idf(words):
    """
    Вычисляет TF-IDF для списка слов.
    """
    word_count = len(words)  # Подсчитываем общее количество слов в тексте
    word_counter = Counter(words)  # Создаем словарь с подсчитанным количеством каждого слова
    data = []  # Создаем пустой список для хранения результатов TF-IDF
    for word, count in word_counter.items():  # Проходим по каждому уникальному слову и его количеству в тексте
        tf = count / word_count  # Вычисляем TF (частоту появления слова) как отношение количества слова к общему числу слов
        idf = math.log(word_count / (1 + count))  # Вычисляем IDF (обратную частоту документов) для каждого слова
        data.append({  # Добавляем результаты вычислений в список data в виде словаря
            'word': word,  # Слово
            'tf': tf,  # TF для слова
            'idf': idf  # IDF для слова
        })
    # Сортировка по убыванию IDF
    data = sorted(data, key=lambda x: x['idf'], reverse=True)  # Сортируем список по убыванию IDF
    return data  # Возвращаем список словарей с результатами TF-IDF, отсортированный по убыванию IDF


def upload_file(request):
    """
    Обрабатывает загруженный файл, вычисляет TF-IDF для слов и возвращает
    результат в виде HTML-страницы.
    """
    if request.method == 'POST':  # Проверяем, был ли отправлен POST-запрос (загрузка файла)
        file = request.FILES.get('file')  # Получаем загруженный файл из запроса
        if file:  # Проверяем, был ли загружен файл
            if file.name.endswith('.txt'):  # Проверяем, что файл имеет расширение .txt
                try:
                    text = file.read().decode('cp1251')  # Читаем содержимое файла в кодировке cp1251
                    if not text:  # Проверяем, что содержимое файла не пустое
                        return HttpResponse('Загруженный файл пуст')
                    words = process_text(text)  # Обрабатываем текст с помощью функции process_text
                    data = calculate_tf_idf(words)  # Вычисляем TF-IDF для обработанных слов
                    return render(
                        request,
                        'word_counter/upload_file.html',
                        {'data': data}
                    )  # Возвращаем HTML-страницу с результатами
                except Exception as e:  # Обрабатываем возможные ошибки
                    return HttpResponse(
                        'Ошибка при обработке файла: {}'.format(e)
                    )
            else:  # Возвращаем сообщение, если файл не в формате .txt
                return HttpResponse(
                    'Пожалуйста, загрузите файл в формате .txt'
                )
        else:  # Возвращаем сообщение, если файл не был загружен
            return HttpResponse('Файл не был загружен')
    return render(request, 'word_counter/upload_file.html')  # Возвращаем страницу загрузки файла для GET-запросов
