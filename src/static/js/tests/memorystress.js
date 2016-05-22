var testTime = 60 * 1000;
var count = 4;
var countHidden = 2;
var maxSymbols = 2; // max = 4
var symbolWidth = 80;
var symbolHeight = 80;
var cellWidth = 120;
var cellHeight = 120;
var cellPadding = 0;
var slideAnim = 1000;
var fillColor = "black";
var random = new Math.seedrandom('SomeSeed');



var startTime;
var symbols = [];
var hiders = [];
var canClick = false;
var group = draw.nested()
    .y("40%")
    .x(- count * (cellWidth + cellPadding) / 2.0 + draw.viewbox().width / 2);
var hiderWidth = cellWidth + cellPadding * 2 + 1;
var hiderHeight = cellHeight + cellPadding * 2;
var hidersShown = false;

for (var i = 0; i < countHidden; i++) {
    var hider = group
        .rect(hiderWidth, hiderHeight)
        .fill("grey")
        .radius(10)
        .x((count - i - 1) * (cellWidth + cellPadding) - cellPadding)
        .y(-cellPadding);
    hider.front().size(hiderWidth, 0); //.opacity(0.9);
    hiders.push(hider);
}

var font = {
    family: 'Georgia',
    size: 48,
    anchor: 'middle',
    leading: 1,
};
var statusText = draw.plain("Совпадает ли первый и последний?")
    .font(font)
    .move("50%", "20%");

var noText = draw.plain("Нет")
    .font(font)
    .move("35%", "80%")
    .style('cursor', 'pointer')
    .click(function(){ click(false); });

var yesText = draw.plain("Да")
    .font(font)
    .move("65%", "80%")
    .style('cursor', 'pointer')
    .click(function(){ click(true); });

function getRandomInt(min, max) {
  return Math.floor(random() * (max - min)) + min;
}

function click(yes) {
    if(!canClick)
        return;

    // First.type == last.type?
    var first = symbols[symbols.length - 1].data('type');
    var last = symbols[0].data('type');

    var data = {
        decisionTime: test.getTime() - startTime,
        choice: yes?'yes':'no',
        first: first,
        last: last
    };

    if( (yes && first == last) ||
        (!yes && first != last)
      ) {
        statusText.plain("Верно");
        test.log("correct", data);
        showHiders();
    }
    else {
        statusText.plain("Не верно");
        test.log("wrong", data);
        hideHiders();
    }

    slide();
    canClick = false;
}

function showHiders() {
    if(!hidersShown)
    {
        hiders.forEach(function(hider) {
            hider.animate(300, '>', 300).size(hiderWidth, hiderHeight);
        });
        hidersShown = true;
    }
}

function hideHiders() {
    if(hidersShown) {
        hiders.forEach(function(hider) {
            hider.animate(300, '>', 300).size(hiderWidth, 1);
        });
        hidersShown = false;
    }
}

function createSymbol() {
    var s;
    var base = group;
    var rnd = getRandomInt(0,maxSymbols);
    if(rnd == 0) s = base.circle(symbolWidth).data('type', 'circe');
    if(rnd == 1) s = base.rect(symbolWidth, symbolHeight).data('type', 'rectangle');
    if(rnd == 2) s = base.polygon('').plot([
        [symbolWidth / 2, 0],
        [symbolWidth, symbolHeight],
        [0, symbolHeight],
    ]).data('type', 'triangle'); // треугольник
    if(rnd == 3) s = base.polygon('').plot([
        [symbolWidth / 2, 0],
        [symbolWidth, symbolHeight / 2],
        [symbolWidth / 2, symbolHeight],
        [0, symbolHeight / 2],
    ]).data('type', 'rhombus'); // ромб

    return s.fill(fillColor).back();
}

function slide() {
    symbols[0].animate(slideAnim).scale(0);
    for (var i = 1; i < symbols.length; i++) {
        symbols[i].animate(slideAnim).dx(cellWidth + cellPadding);
    }

    setTimeout(slideEnd, slideAnim);
}

function slideEnd() {
    statusText.plain("Совпадает ли первый и последний?");

    var s = createSymbol()
        .dx((cellWidth - symbolWidth) * 0.5)
        .dy((cellHeight - symbolHeight) * 0.5);
    symbols.push(s);

    if(symbols.length > count) {
        symbols[0].remove();
        symbols.shift();
    }
    startTime = test.getTime();
    canClick = true;
}

test.on("start", function() {
    for (var i = 0; i < count; i++) {
        var s = createSymbol()
            .x((count - i - 1) * (cellWidth + cellPadding) + (cellWidth - symbolWidth) * 0.5)
            .y((cellHeight - symbolHeight) * 0.5);
        symbols.push(s);
    }
    canClick = true;
    startTime = test.getTime();
    setTimeout(function() {
        canClick = false;
        test.complete();
    }, testTime)
});