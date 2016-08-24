
class CognitiveTest:
    all = {}

    def __init__(self, name):
        self.name = name
        self.title = ''
        self.record_audio = True
        self.record_video = False
        self.record_mouse = True
        self.scripts = []
        self.instructions = ''
        self.version = '0.1'

    @classmethod
    def get(cls, name):
        return CognitiveTest.all[name]

    @classmethod
    def add(cls, test):
        CognitiveTest.all[test.name] = test


test = CognitiveTest('temperament')
test.title = u"Тест на темперамент"
test.instructions = 'Вам предлагается ответить на 57 вопросов. Вопросы направлены на выявление вашего обычного способа поведения. Постарайтесь представить типичные ситуации и дайте первый «естественный» ответ, который придет вам в голову. Если вы согласны с утверждением, нажмите «да», если нет — «нет».'
test.record_audio = False
test.record_mouse = False
test.record_video = False
test.scripts = ["tests/temperament.js"]

CognitiveTest.add(test)

test = CognitiveTest('reading')
test.title = "«Бегущая строка»"
test.instructions = "Вам представлен текст в формате быстрой бегущей строки. Ваша задача – правильно прочитать текст вслух."
test.record_audio = True
test.record_mouse = False
test.record_video = False
test.scripts = ["tests/reading.js"]

CognitiveTest.add(test)
