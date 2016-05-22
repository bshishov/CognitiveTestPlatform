var colors = ['red', 'green', 'yellow', 'cyan', 'blue'];
var colorNames = ['красный', 'зеленый', 'желтый', 'голубой', 'синий'];
var colorButtonRadius = 100;
var colorButtonPadding = 100;
var startTimeout = 2000;
var attempts = 10;
var random = new Math.seedrandom('123');


var speechRecognitionAvailable = (SpeechRecognition != undefined) || ('webkitSpeechRecognition' in window) || false;
//var showControls = true; // = !speechRecognitionAvailable;
var showControls = !speechRecognitionAvailable;

var current;
var currentAttempt = 0;
var canSelect = false;
var showTime;

var colorText = draw.plain("").move('50%', '55%');
colorText.font({
    family: 'Georgia',
    size: 72,
    anchor: 'middle',
    leading: 1,
});

var statusText = draw.plain("").move('50%', '20%');
statusText.font({
    family: 'Georgia',
    size: 48,
    anchor: 'middle',
    leading: 1,
});

var controlsFont = {
    family: 'Georgia',
    size: 32,
    anchor: 'middle',
    leading: 1,
};


function getRandomInt(min, max) {
  return Math.floor(random() * (max - min)) + min;
}

function getRandomText() {
    var colorIndex = getRandomInt(0, colors.length);

    return {
        text: colorNames[getRandomInt(0, colorNames.length)],
        color: colors[colorIndex],
        colorName: colorNames[colorIndex]
    };
}

function select(colorName) {
    if(!canSelect)
        return;

    if(colorNames.indexOf(colorName) < 0)
        return;

    currentAttempt++;
    var reactionTime = test.getTime() - showTime;
    var logData = {
            "reaction": reactionTime,
            "current": current,
            "selected": colorName
        };

    if(current.colorName == colorName) {
        test.log("correct", logData);
        statusText.plain("Верно!");
    }
    else {
        test.log("wrong", logData);
        statusText.plain("Не верно!");
    }
    canSelect = false;

    if(currentAttempt < attempts)
        setTimeout(start, startTimeout);
    else
        test.complete();
}

function start() {
    statusText.plain("Назовите цвет надписи?");
    canSelect = true;

    current = getRandomText();
    colorText.plain(current.text.capitalizeFirstLetter());
    colorText.fill(current.color);
    showTime = test.getTime();

    test.log('start');
}

test.on("start", function() {
    start();
});


// Если недоспно API распознавания голоса то использовать контролы
if(showControls)
{
    var group = draw.nested();

    for (var i = 0; i < colors.length; i++) {
        let colorName = colorNames[i];
        //group.circle(colorButtonRadius)
        group.plain(colorName)
            .font(controlsFont)

            .click(function() {
                console.log("click", colorName);
                select(colorName);
            })
            //.fill(colors[i])
            .style('cursor', 'pointer')
            .x((i - (colors.length - 1) / 2.0) * (colorButtonRadius + colorButtonPadding));
    }

    group.move("50%", "80%");
}


if(speechRecognitionAvailable)
{
    // За основу взят код:
    // https://github.com/mdn/web-speech-api/blob/master/speech-color-changer/script.js
    // Работает только в последних версиях Chrome / Firefox
    var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
    var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList;
    var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent;

    var grammar = '#JSGF V1.0; grammar colors; public <color> = красный | синий | зеленый | желтый ;'
    var recognition = new SpeechRecognition();
    var speechRecognitionList = new SpeechGrammarList();
    speechRecognitionList.addFromString(grammar, 1);
    recognition.grammars = speechRecognitionList;
    recognition.continuous = false;
    recognition.lang = 'ru-RU';
    //recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = function(event) {
      // The SpeechRecognitionEvent results property returns a SpeechRecognitionResultList object
      // The SpeechRecognitionResultList object contains SpeechRecognitionResult objects.
      // It has a getter so it can be accessed like an array
      // The first [0] returns the SpeechRecognitionResult at position 0.
      // Each SpeechRecognitionResult object contains SpeechRecognitionAlternative objects that contain individual results.
      // These also have getters so they can be accessed like arrays.
      // The second [0] returns the SpeechRecognitionAlternative at position 0.
      // We then return the transcript property of the SpeechRecognitionAlternative object
      var color = event.results[0][0].transcript;
      //diagnostic.textContent = 'Result received: ' + color + '.';
      //bg.style.backgroundColor = color;
        if(colorNames.indexOf(color) >= 0) {
            select(color);
        }
        else {
            var found = false;
            colorNames.forEach(function(e) {
                if(color.indexOf(e) > -1){
                    found = true;
                    select(e);
                }
            });

            if(!found){
                statusText.plain("Не могу распознать");
                test.log("notrecognized", color);
                recognition.stop();
            }
        }
      console.log(color, 'Confidence: ' + event.results[0][0].confidence);
    }

    recognition.onspeechend = function() {
        console.log('speech end');
        recognition.stop();
    }

    recognition.onnomatch = function(event) {
        console.log('no match');
        statusText.plain("Не могу распознать");
        test.log("notrecognized");
        recognition.stop();
    }

    recognition.onerror = function(event) {
        console.log('Error occurred in recognition: ', event.error);
    }

    recognition.onend = function(event) {
        console.log('Recognition ended');

        // Restarting
        recognition.start();
    }

    recognition.start();
}

String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}