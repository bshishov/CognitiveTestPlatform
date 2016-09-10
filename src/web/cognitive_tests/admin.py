from django.contrib import admin
from .models import *
from django_ace import AceWidget
from django.contrib.admin.widgets import FilteredSelectMultiple


admin.site.site_header = 'Платформа для тестирования'


@admin.register(Test)
class AdminTest(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'active')
    list_filter = ('active',)
    search_fields = ['name']


@admin.register(WebTest)
class AdminWebTest(admin.ModelAdmin):
    class WebTestResourcesInline(admin.TabularInline):
        model = WebTest.resources.through
        extra = 0

    list_display = ('test', 'group', 'order', 'record_audio', 'record_video', 'record_mouse', 'created', 'test_active',)
    list_filter = ('test__active', 'group',)

    formfield_overrides = {
        models.TextField: {'widget': AceWidget(theme='github', width="100%", mode='javascript', height='500px')},
    }

    def test_name(self, obj):
        return obj.test.name

    def test_active(self, obj):
        return obj.test.active

    exclude = ('resources',)
    search_fields = ['test__name']
    inlines = [WebTestResourcesInline, ]


class AdminTestFileInline(admin.TabularInline):
    model = TestFile
    extra = 0


class AdminTestTextDataInline(admin.TabularInline):
    model = TestTextData
    extra = 0


@admin.register(Participant)
class AdminParticipant(admin.ModelAdmin):
    list_display = ('name', 'user', 'age', 'gender', 'allow_info_usage', 'email', 'created')
    list_filter = ('name', 'user', 'age', 'gender', 'allow_info_usage', 'email')
    search_fields = ['name']


@admin.register(TestResult)
class AdminTestResult(admin.ModelAdmin):
    list_display = ('participant', 'test', 'created',)
    list_filter = ('participant', 'test',)
    inlines = [AdminTestFileInline, AdminTestTextDataInline,]


@admin.register(TestFile)
class AdminTestFile(admin.ModelAdmin):
    list_display = ('name', 'test_result', 'file', 'created')
    list_filter = ('name', 'test_result',)
    search_fields = ['name']

    def created(self, obj):
        return obj.test_result.created

    created.short_description = 'Создан'
    created.admin_order_field = 'test_result__created'


@admin.register(WebTestResource)
class AdminWebTestResource(admin.ModelAdmin):
    list_display = ('file', 'extension', )


@admin.register(TestTextData)
class AdminTestTextData(admin.ModelAdmin):
    list_display = ('name', 'test_result', 'data_truncated', 'created')
    list_filter = ('name', 'test_result',)
    search_fields = ['name']

    def data_truncated(self, obj):
        data = obj.data
        return (data[:75] + '...') if len(data) > 150 else data

    data_truncated.short_description = 'Data'

    def created(self, obj):
        return obj.test_result.created

    created.short_description = 'Создан'
    created.admin_order_field = 'test_result__created'

    formfield_overrides = {
        models.TextField: {'widget': AceWidget(theme='github', width="100%", mode='json', height='500px')},
    }


@admin.register(WebTestGroup)
class AdminWebTestGroup(admin.ModelAdmin):
    class AdminGroupResourcesInline(admin.TabularInline):
        model = WebTestGroup.resources.through
        extra = 0

    class AdminWebTestsInline(admin.TabularInline):
        fields = ('test',)
        model = WebTest
        extra = 0

    exclude = ('resources',)  # editing via inline
    list_display = ('name', 'description',)
    search_fields = ['name']
    inlines = [AdminWebTestsInline, AdminGroupResourcesInline, ]
