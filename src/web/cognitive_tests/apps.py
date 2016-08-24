from django.apps import AppConfig


class CognitiveTestsConfig(AppConfig):
    name = 'cognitive_tests'
    verbose_name = 'Cognitive Tests'

    tests = [
        {
            "id": "temperament",
            "version": "0.1",
            "name": "Тест на темперамент",
            "instructions": "Вам предлагается ответить на 57 вопросов. Вопросы направлены на выявление вашего обычного способа поведения. Постарайтесь представить типичные ситуации и дайте первый «естественный» ответ, который придет вам в голову. Если вы согласны с утверждением, нажмите «да», если нет — «нет».",
            "record_audio": False,
            "record_video": False,
            "record_mouse": False,
            "scripts": ["tests/temperament.js"]
        },
        {
            "id": "reading",
            "version": "0.1",
            "name": "«Бегущая строка»",
            "instructions": "Вам представлен текст в формате быстрой бегущей строки. Ваша задача – правильно прочитать текст вслух.",
            "record_audio": True,
            "record_video": False,
            "record_mouse": True,
            "scripts": ["tests/reading.js"]
        },
        {
            "id": "reaction",
            "version": "0.1",
            "name": "Тест на скорость реакции",
            "instructions": "Это тест для измерения скорости вашей реакции. Когда на экране появится темный круг – вы должны кликнуть по нему. Будьте внимательны! Два фальстарта сбросят ваш результат.",
            "record_audio": False,
            "record_video": False,
            "record_mouse": True,
            "scripts": ["tests/reaction.js"]
        },
        {
            "id": "plasticity",
            "version": "0.1",
            "name": "Тест на пластичность",
            "instructions": "Вам предлагаются сочетания названий основных цветов, где значение слова и цвет шрифта частью совпадают, частью нет. Нужно быстро читать про себя слова и называть вслух цвет шрифта.",
            "record_audio": True,
            "record_video": False,
            "record_mouse": True,
            "scripts": ["tests/plasticity.js"]
        },
        {
            "id": "operation",
            "version": "0.1",
            "name": "Тест на оперативность мышления",
            "instructions": "Вам предлагается два числовых выражения, нужно выбрать наибольшее по значению и кликнуть на него. Тест не ограничен по времени, однако его продолжительность влияет на полученные вами баллы.",
            "record_audio": False,
            "record_video": False,
            "record_mouse": True,
            "scripts": ["tests/operation.js"]
        },
        {
            "id": "memory",
            "version": "0.1",
            "name": "Тест для оценки памяти",
            "instructions": "Вам будут предлагаться различные изображения, всегда нужно выбирать то изображение, которое вы не выбирали до этого. Не торопитесь, этот тест НЕ на скорость, а на внимательность.",
            "record_audio": False,
            "record_video": False,
            "record_mouse": True,
            "scripts": ["tests/memory.js"]
        },
        {
            "id": "memorystress",
            "version": "0.1",
            "name": "Тест на память в стрессовой ситуации",
            "instructions": "Вам предлагаются 4 квадрата с изображениями. Если изображения в квадрате 1 и 4 совпадают -  нажимайте «ДА», если не совпадают – «НЕТ». Этот тест на время – постарайтесь отвечать быстро и правильно.",
            "record_audio": False,
            "record_video": False,
            "record_mouse": True,
            "scripts": ["tests/memorystress.js"]
        },
    ]