var startSpeed = 5;
var endSpeed = 15;
var startPosition = 1000;

var text = "Немногим более 50 лет прошло с тех пор, как появилась первая электронная вычислительная машина. За этот короткий для развития общества период сменилось несколько поколений вычислительных машин, а первые ЭВМ сегодня являются музейной редкостью. Сама история развития вычислительной техники представляет немалый интерес, показывая тесную взаимосвязь математики с физикой (прежде всего с физикой твердого тела, полупроводников, электроникой) и современной технологией, уровнем развития которой во многом определяется прогресс в производстве средств вычислительной техники.";

var isAnimating = false;
var textObject = draw.plain(text).move(1000, '50%')
textObject.font({
    family: 'Georgia',
    size: 48,
    anchor: 'left',
    leading: 1,
});

var width = textObject.length();

var progress = function() {
    return Math.abs(textObject.x() - startPosition) / (width + startPosition);
}

var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
                          window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;


var move = function() {
    var p = progress();
    var speed = startSpeed + p * (endSpeed - startSpeed);

    textObject.dx(-speed);
    if(p > 1.0) {
        complete();
    }
};

var complete = function() {
    isAnimating = false;
    test.complete();
}

var anim = function(timestamp) {
    if(isAnimating) {
        move();
        requestAnimationFrame(anim);
    }
}

test.on("start", function() {
    textObject.move(1000, '50%');
    requestAnimationFrame(anim);
    isAnimating = true;
});