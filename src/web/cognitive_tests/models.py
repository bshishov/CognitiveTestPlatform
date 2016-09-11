from django.db import models
import os


class Participant(models.Model):
    PARTICIPANT_SESSION_KEY = 'participant_id'
    GENDER_CHOICES = (
        (True, 'Male'),
        (False, 'Female')
    )
    user = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='Пользователь')
    last_test = models.CharField(max_length=255, verbose_name='Последний тест', blank=True, null=True)
    session = models.CharField(max_length=1000, verbose_name='Ключ сессии')
    name = models.CharField(max_length=255, verbose_name='Имя')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')
    gender = models.BooleanField(choices=GENDER_CHOICES, verbose_name='Пол')
    allow_info_usage = models.BooleanField(verbose_name='Разрешение на публикацию данных')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):  # __unicode__ on Python 2
        return "%s %s" % (self.name, self.age)


class Test(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    active = models.BooleanField(default=True, verbose_name='Активен')
    auto_save_data_to_file = models.BooleanField(default=False, verbose_name='Автоматически сохранять данные в файлы')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.name


class TestResult(models.Model):
    participant = models.ForeignKey(Participant, related_name='test_results', on_delete=models.CASCADE,
                                    verbose_name='Участник')
    test = models.ForeignKey(Test, related_name='test_results', verbose_name='Тест')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):  # __unicode__ on Python 2
        return "%s (%s)" % (self.test, self.participant)

    class Meta:
        verbose_name = 'Результаты'
        verbose_name_plural = 'Результаты'


class TestFile(models.Model):
    def get_filename(self, filename):
        url = "results/test_%s/participant_%s/raw/%s" % (self.test_result.test.id, self.test_result.participant.id, filename)
        return url

    name = models.CharField(max_length=255, verbose_name='Имя файла')
    test_result = models.ForeignKey(TestResult, related_name='files', on_delete=models.CASCADE,
                                    verbose_name='Результат')
    file = models.FileField(upload_to=get_filename, verbose_name='Файл')

    class Meta:
        verbose_name = 'Файлы результата'
        verbose_name_plural = 'Файлы результатов'

    def __str__(self):  # __unicode__ on Python 2
        return "%s (%s)" % (self.name, self.test_result)


class TestTextData(models.Model):
    RESTRICTED_NAMES = ('id', 'csrfmiddlewaretoken')

    name = models.CharField(max_length=255, verbose_name='Имя данных')
    test_result = models.ForeignKey(TestResult, related_name='text_data', on_delete=models.CASCADE, verbose_name='Результат')
    data = models.TextField(verbose_name='Данные')

    def __str__(self):  # __unicode__ on Python 2
        return "%s (%s)" % (self.name, self.test_result)

    class Meta:
        verbose_name = 'Данные результата'
        verbose_name_plural = 'Данные результатов'


class WebTestResource(models.Model):
    file = models.FileField(upload_to='resources', verbose_name='Файл')

    @property
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.file.name


class WebTestGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание (markdown)', blank=True)
    resources = models.ManyToManyField(WebTestResource, verbose_name='Ресурсы')

    class Meta:
        verbose_name = 'Группа веб тестов'
        verbose_name_plural = 'Группы веб тестов'

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.name


class WebTest(models.Model):
    test = models.OneToOneField(Test, related_name='web_test', verbose_name='Тест')
    group = models.ForeignKey(WebTestGroup, verbose_name='Группа', related_name='Тесты')
    order = models.PositiveIntegerField(verbose_name='Порядок в группе')
    instructions = models.TextField(verbose_name='Инструкция (markdown)', blank=True)
    js_inline_script = models.TextField(blank=True, null=True, verbose_name='JS скрипт')
    record_audio = models.BooleanField(default=False, verbose_name='Записывать аудио')
    record_video = models.BooleanField(default=False, verbose_name='Записывать видео')
    record_mouse = models.BooleanField(default=False, verbose_name='Записывать события мыши')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    resources = models.ManyToManyField('WebTestResource')

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.test

    class Meta:
        ordering = ['-order']
        verbose_name = 'Веб тест'
        verbose_name_plural = 'Веб тесты'



