import speech_recognition as sr
import os
import argparse

# Функция, позволяющая проговаривать слова
# Принимает параметр "Слова" и прогроваривает их


def talk(words):
    print(words)  # Дополнительно выводим на экран
    os.system("espeak '" + words + "' --stdout|aplay")  # Проговариваем слова


"""
    Функция get_command() служит для отслеживания микрофона.
    Вызывая функцию мы будет слушать что скажет пользователь,
    при этом для прослушивания будет использован микрофон.
    Получение данные будут сконвертированы в строку и далее
    будет происходить их проверка.
"""


def get_command(recognizer):
    talk('start')

    # Создаем объект на основе библиотеки
    # speech_recognition и вызываем метод для определения данных
    r = sr.Recognizer()

    # Начинаем прослушивать микрофон и записываем данные в source
    with sr.Microphone() as source:
        # Просто вывод, чтобы мы знали когда говорить
        print("Говорите")
        # Устанавливаем паузу, чтобы прослушивание
        # началось лишь по прошествию 1 секунды
        r.pause_threshold = 1
        # используем adjust_for_ambient_noise для удаления
        # посторонних шумов из аудио дорожки
        r.adjust_for_ambient_noise(source, duration=1)
        # Полученные данные записываем в переменную audio
        # пока мы получили лишь mp3 звук
        audio = r.listen(source)
        talk('end')

    try:  # Обрабатываем все при помощи исключений
        """
        Распознаем данные из mp3 дорожки.
        Указываем что отслеживаемый язык русский.
        Благодаря lower() приводим все в нижний регистр.
        Теперь мы получили данные в формате строки,
        которые спокойно можем проверить в условиях
        """
        if recognizer == 'google':
            sample = r.recognize_google(audio, language="en-US").lower()
        elif recognizer == 'sphinx':
            keywords = [('show', 1), ('box', 1), ('number', 1), ('forward', 1), ('correct', 0.6),
                        ('wrong', 0.6)]
            sample = r.recognize_sphinx(audio, keyword_entries=keywords)
        # Просто отображаем текст что сказал пользователь
        print("Вы сказали: " + sample)
    # Если не смогли распознать текст, то будет вызвана эта ошибка
    except sr.UnknownValueError:
        # Здесь просто проговариваем слова "Я вас не поняла"
        # и вызываем снова функцию get_command() для
        # получения текста от пользователя
        talk("wuf wuf")
        sample = get_command(recognizer)

    # В конце функции возвращаем текст задания
    # или же повторный вызов функции
    return sample


# функция получения согласия или несогласия от ведущего
def get_confirmation():
    while True:
        sample = get_command()
        if any([com in sample for com in correct_com]):
            return 1
        elif any([com in sample for com in wrong_com]):
            return 0


# варианты команды ввода нномера коробки
box_com = ['show box', 'box number', 'showbox', 'show number', 'show', 'books', 'books number',
           'number', 'phone']

# варианты номеров
num_coms = [['1', 'one', 'won'], ['2', 'two', 'too', 'to'], ['3', 'tree', 'three', 'free'],
            ['4', 'four', 'for']]

# варианты согласия
correct_com = ['right', 'yes', 'correct']

# варианты несогласия
wrong_com = ['wrong', 'no', 'not right', 'not correct']

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-r', "--recognizer", type=str, default='sphinx',
                    help="recognizer type, google or sphinx")
    args = vars(ap.parse_args())
    while True:
        get_command(args['recognizer'])
