var startTimeout = 1000;
var startCount = 3;
var imageWidth = 90;
var imageHeight = 90;
var imagePadding = 30;
var maxInRow = 6;
var random = new Math.seedrandom('SomeSeed');
var images = [
    'alarm-clock',
    'avatar',
    'brain',
    'coffee-cup',
    'binoculars',
    'clock',
    'cogwheel',
    'phone-call',
    'rocket',
    'mortarboard',
    'shoe',
    'paper-plane',
    'puzzle',
    'compass',
    'flag',
    'balance',
];

var canClick = false;
var selected = [];
var count = startCount;
var startTime;
var currentGroup;
var statusFont = {
    family: 'Georgia',
    size: 36,
    anchor: 'middle',
    leading: 1,
};
var statusText = draw.plain("")
    .move('50%', '20%')
    .font(statusFont);


function getRandomInt(min, max) {
  return Math.floor(random() * (max - min)) + min;
}

function getRandomIntegers(count, min, max) {
    if(count <= 0) return [];
    if(count == 1) return getRandomInt(min, max);
    if(max - min < count){
        console.error("Can't create this amout of random integers");
        return [];
    }

    var result = [getRandomInt(min, max)];
    let val;
    for (var i = 1; i < count; i++) {
        do {
            val = getRandomInt(min, max);
        } while(result.indexOf(val) != -1)
        result.push(val);
    }
    return result;
}

function getRandomImages(count) {
    var rnd = getRandomIntegers(count, 0, images.length);
    var rndImages = [];
    var hasUnselected = false;
    for (var i = 0; i < rnd.length; i++) {
        var img = images[rnd[i]];
        if(selected.indexOf(img) == -1)
            hasUnselected = true;
        rndImages.push(img);
    }

    if(hasUnselected)
        return rndImages;
    else
        return getRandomImages(count); // try again
}

function getImagePath(name) {
    return "/static/img/tests/memory/" + name + ".png";
}

function click(name) {
    if(!canClick)
        return;

    var reactionTime = test.getTime() - startTime;
    var data = {
        image: name,
        reaction: reactionTime,
        remembered: selected.length
    };

    if(selected.indexOf(name) > -1) {
        statusText.plain("Не верно");
        test.log("fail", data);
        test.complete();
        return;
    }
    else {
        statusText.plain("Хорошо");
        test.log("success", data);
        selected.push(name);
    }

    canClick = false;
    count++;
    if(count > images.length - 1)
        test.complete();
    else
        setTimeout(start, startTimeout);
}

function start() {
    if(currentGroup != undefined)
        currentGroup.remove();
    statusText.plain("Выберите картинку, которую Вы еще не выбирали");
    currentGroup = draw.nested();
    var rnd = getRandomImages(count)
    var imagesToShow = [];
    for (var i = 0; i < count; i++) {
        let img = rnd[i];
        imagesToShow.push(img);
        // positioning
        let col = i % maxInRow;
        let row = Math.floor(i / maxInRow);
        let rows = Math.floor(count / maxInRow);
        let cols = i < rows * maxInRow ? maxInRow : count - row * maxInRow;

        currentGroup.image(getImagePath(img))
            .size(imageWidth, imageHeight)
            .click(function() { click(img); })
            .style('cursor', 'pointer')
            .y(row * (imageHeight + imagePadding))
            .x((col - cols / 2.0) * (imageWidth + imagePadding));
    }
    currentGroup
        //.x(draw.viewbox().width / 2 - currentGroup.bbox().width / 2)
        .x(draw.viewbox().width / 2)
        .y(draw.viewbox().height / 2 - currentGroup.bbox().height / 2 + imagePadding * 2);
    canClick = true;
    startTime = test.getTime();
    test.log("show", imagesToShow)
}

test.on('start', function() {
    start();
});