var text = "Выросла на краю поляны Крапива. Поднялась над травами и смутилась. Цветы вокруг красивые и душистые, ягоды вкусные.  Ни вкуса приятного, ни яркого цвета, ни сладкого запаха у неё нет! \
— Будто меня и не было совсем, будто я и не жила! Пропади пропадом такое крапивное счастье!";

var textObject = draw.plain(text).move(1000, '50%')
textObject.font({
    family: 'Georgia',
    size: 48,
    anchor: 'left',
    leading: 1,
});
//textObject.rebuild(false);
var width = textObject.length();

test.on("start", function() {
    textObject.move(1000, '50%');
    textObject.animate('10s').x(-width + 100).after(function() {
        test.complete();
    });
});