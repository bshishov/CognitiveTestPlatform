from django.db import models


class Participant(models.Model):
    user = models.ForeignKey('auth.User', blank=True, null=True)
    last_test = models.CharField(max_length=255)
    session = models.CharField(max_length=1000)
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    gender = models.BooleanField()
    allow_info_usage = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=1000)

    def __str__(self):  # __unicode__ on Python 2
        return "%s %s" % (self.name, self.age)


class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    enabled = models.BooleanField(default=True)
    auto_save_data_to_file = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.name


class WebTest(models.Model):
    from .utils import SeparatedValuesField

    test = models.OneToOneField(Test, related_name='web_test')
    record_audio = models.BooleanField(default=False)
    record_video = models.BooleanField(default=False)
    record_mouse = models.BooleanField(default=False)
    resources_path = models.CharField(max_length=1024, blank=True, null=True)
    js_inline_script = models.TextField(blank=True, null=True)
    js_script_files = SeparatedValuesField(max_length=1024, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.test


class TestResult(models.Model):
    participant = models.ForeignKey(Participant, related_name='test_results')
    test = models.ForeignKey(Test, related_name='test_results')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return "%s" % self.participant


class TestFile(models.Model):
    def get_filename(self, filename):
        url = "results/test/%s/%s/raw/%s" % (self.test_result.test.id, self.test_result.participant.id, filename)
        return url

    name = models.CharField(max_length=255)
    test_result = models.ForeignKey(TestResult, related_name='files')
    file = models.FileField(upload_to=get_filename)
    created = models.DateTimeField(auto_now_add=True)


class TestTextData(models.Model):
    name = models.CharField(max_length=255)
    test_result = models.ForeignKey(TestResult, related_name='text_data')
    data = models.TextField()
    created = models.DateTimeField(auto_now_add=True)



