// OPTIONS
var minAttemtps = 10; // minimum of successfull attempts
var waitAfterResult = 3500; //ms
var minWaitBeforeShow = 1000; //ms
var maxWaitBeforeShow = 3000; //ms
var random = new Math.seedrandom('someRandomSeed');


var canClick = false;
var showTime;
var succeeds = 0;

function getRandomInt(min, max) {
  return Math.floor(random() * (max - min)) + min;
}

var success = function() {
    canClick = false;
    var reactionTime = test.getTime() - showTime;

    test.log('success', { reaction: reactionTime });
    circle.fill('green');

    statusText.plain("Отлично!");
    statusText.fill("green");

    reactionText.plain("Реакция: " + reactionTime + "мс");

    succeeds++;
    if(succeeds >= minAttemtps){
        test.complete();
    } else {
        // start again after 2sec
        setTimeout(start, waitAfterResult);
    }
};

var fail = function() {
    canClick = false;

    test.log('fail');
    circle.fill('red');

    statusText.plain("Слишком рано! ");
    statusText.fill("red");

    // start again after 2sec
    setTimeout(start, waitAfterResult);
};

var circleClick = function() {
    if(!canClick)
        return;

    success();
};

var backgroundClick = function() {
    fail();
};

var bgr = draw.circle(210)
    .center('50%', '50%')
    .fill('white')
    .stroke('black')
    .style('cursor', 'pointer')
    .click(backgroundClick);

var circle = draw.circle(200)
    .center('50%', '50%')
    .fill('black')
    .style('cursor', 'pointer')
    .click(circleClick)
    .hide();

var statusText = draw.plain("Приготовься").move('50%', '20%');
statusText.font({
    family: 'Georgia',
    size: 48,
    anchor: 'middle',
    leading: 1,
});

var reactionText = draw.plain("").move('50%', '85%');
reactionText.font({
    family: 'Georgia',
    size: 24,
    anchor: 'middle',
    leading: 1,
});

// start sequence
var start = function() {
    reactionText.plain("");
    statusText.plain("Приготовься");
    statusText.fill("black");


    canClick = true;
    circle.hide();
    circle.fill('black');

    var delay = getRandomInt(minWaitBeforeShow, maxWaitBeforeShow);
    test.log('start', { showDelay: delay });
    setTimeout(show, delay);
};

// show circle
var show = function() {
    test.log('show');
    circle.show();
    showTime = test.getTime();

    if(canClick)
        statusText.plain("Жми!");
};

test.on("start", function() {
    start();
});