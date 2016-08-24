var startTimeout = 1000;
var random = new Math.seedrandom('SomeSeed');
var expressions = [
    {
        left: "11",
        right: "13"
    },
    {
        left: "15",
        right: "18"
    },
    {
        left: "14",
        right: "13"
    },
    {
        left: "43",
        right: "34"
    },
    {
        left: "16",
        right: "15 "
    },
    {
        left: "24-3",
        right: "20+2"
    },
    {
        left: "17+2",
        right: "19-1"
    },
    {
        left: "13+5",
        right: "15+4"
    },
    {
        left: "22+4",
        right: "28-3"
    },
    {
        left: "11+6",
        right: "14+4"
    },
    {
        left: "21-3",
        right: "14+3"
    },
    {
        left: "17+9",
        right: "23+4"
    },
    {
        left: "26+7",
        right: "39-5"
    },
    {
        left: "33-8",
        right: "23+3"
    },
    {
        left: "13+14",
        right: "38-12"
    },
    {
        left: "2+2*8",
        right: "(7-4)*5"
    },
    {
        left: "27-13+4",
        right: "28/2+3"
    },
    {
        left: "(15-4)*3",
        right: "4*4*2"
    },
    {
        left: "24/3+14",
        right: "4*8-12"
    },
    {
        left: "(17-5)/3*7",
        right: "(9+6)*2+4 "
    },
];

var current = 10;
var currentPair;
var canClick = false;
var startTime;


// for left button isRight == false
// for right button isRight == true
function click(isRight) {
    if(!canClick)
        return;

    var reactionTime = test.getTime() - startTime;
    var data = {
        reaction : reactionTime,
        choice: isRight ? "right" : "left"
    };

    if(
        (isRight == true && currentPair.rightResult > currentPair.leftResult) ||
        (isRight == false && currentPair.leftResult > currentPair.rightResult)
        ) {
        statusText.plain("Верно");
        test.log("correct", data);
    }
    else {
        statusText.plain("Не верно");
        test.log("wrong", data);
    }


    canClick = false;
    setTimeout(start, startTimeout);
}


var font = {
    family: 'Georgia',
    size: 72,
    anchor: 'middle',
    leading: 1,
};

var statusFont = {
    family: 'Georgia',
    size: 48,
    anchor: 'middle',
    leading: 1,
};

var statusText = draw.plain("")
    .font(statusFont)
    .move("50%", "20%");

var leftExpr = draw.plain("")
    .font(font)
    .move("30%", "55%")
    .style('cursor', 'pointer')
    .click(function(){ click(false); });

var rightExpr = draw.plain("")
    .font(font)
    .move("70%", "55%")
    .style('cursor', 'pointer')
    .click(function(){ click(true); });


function start() {
    if(current >= expressions.length)
    {
        test.complete();
        return;
    }

    var raw = expressions[current];

    // Swap left and right 50/50
    if(random() < 0.5) {
        currentPair = {
            left: raw.right,
            right: raw.left
        }
        console.log("swapped");
    }
    else {
        currentPair = raw;
    }

    currentPair.leftResult = eval(currentPair.left);
    currentPair.rightResult = eval(currentPair.right);

    leftExpr.plain(currentPair.left);
    rightExpr.plain(currentPair.right);
    statusText.plain("Какое выражение больше?");
    canClick = true;
    startTime = test.getTime();
    test.log("start", currentPair);

    current++;
}

test.on("start", function() {
    start();
});

