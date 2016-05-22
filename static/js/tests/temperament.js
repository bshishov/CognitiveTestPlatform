var splitBy = 30;
var questions = [
    { id: 1,  question: "Нравится ли вам оживление и суета вокруг вас?" },
    { id: 2,  question: "Часто ли у вас бывает беспокойное чувство, что вам что-нибудь хочется, а вы не знаете что?" },
    { id: 3,  question: "Вы из тех людей, которые не лезут за словом в карман?" },
    { id: 4,  question: "Чувствуете ли вы себя иногда счастливым, а иногда печальным без какой-либо причины?" },
    { id: 5,  question: "Держитесь ли вы обычно в тени на вечеринках или в компании?" },
    { id: 6,  question: "Всегда ли в детстве вы делали немедленно и безропотно то, что вам приказывали?" },
    { id: 7,  question: "Бывает ли у вас иногда дурное настроение?" },
    { id: 8,  question: "Когда вас втягивают в ссору, предпочитаете ли вы отмолчаться, надеясь, что все обойдется?" },
    { id: 9,  question: "Легко ли вы поддаетесь переменам настроения?" },
    { id: 10, question: "Нравится ли вам находиться среди людей?" },
    { id: 11, question: "Часто ли вы теряли сон из-за своих тревог?" },
    { id: 12, question: "Упрямитесь ли вы иногда?" },
    { id: 13, question: "Могли бы вы назвать себя бесчестным?" },
    { id: 14, question: "Часто ли вам приходят хорошие мысли слишком поздно?" },
    { id: 15, question: "Предпочитаете ли вы работать в одиночестве?" },
    { id: 16, question: "Часто ли вы чувствуете себя апатичным и усталым без серьезной причины?" },
    { id: 17, question: "Вы по натуре живой человек?" },
    { id: 18, question: "Смеетесь ли вы иногда над неприличными шутками?" },
    { id: 19, question: "Часто ли вам что-то так надоедает, что вы чувствуете себя «сытым по горло»?" },
    { id: 20, question: "Чувствуете ли вы себя неловко в какой-либо одежде, кроме повседневной?" },
    { id: 21, question: "Часто ли ваши мысли отвлекаются, когда вы пытаетесь сосредоточиться на чем-то?" },
    { id: 22, question: "Можете ли вы быстро выразить ваши мысли словами?" },
    { id: 23, question: "Часто ли вы бываете погружены в свои мысли?" },
    { id: 24, question: "Полностью ли вы свободны от всяких предрассудков?" },
    { id: 25, question: "Нравятся ли вам первоапрельские шутки?" },
    { id: 26, question: "Часто ли вы думаете о своей работе?" },
    { id: 27, question: "Очень ли вы любите вкусно поесть?" },
    { id: 28, question: "Нуждаетесь ли вы в дружески расположенном человеке, чтобы выговориться, когда вы раздражены?" },
    { id: 29, question: "Очень ли вам неприятно брать взаймы или продавать что-нибудь, когда вы нуждаетесь в деньгах?" },
    { id: 30, question: "Хвастаетесь ли вы иногда?" },
    { id: 31, question: "Очень ли вы чувствительны к некоторым вещам?" },
    { id: 32, question: "Предпочли бы вы остаться в одиночестве дома, чем пойти на скучную вечеринку?" },
    { id: 33, question: "Бываете ли вы иногда беспокойными настолько, что не можете долго усидеть на месте?" },
    { id: 34, question: "Склонны ли вы планировать свои дела тщательно и раньше чем следовало бы?" },
    { id: 35, question: "Бывают ли у вас головокружения?" },
    { id: 36, question: "Всегда ли вы отвечаете на письма сразу после прочтения?" },
    { id: 37, question: "Справляетесь ли вы с делом лучше, обдумав его самостоятельно, а не обсуждая с другими?" },
    { id: 38, question: "Бывает ли у вас когда-либо одышка, даже если вы не делали никакой тяжелой работы?" },
    { id: 39, question: "Можно ли сказать, что вы человек, которого не волнует, чтобы все было именно так, как нужно?" },
    { id: 40, question: "Беспокоят ли вас ваши нервы?" },
    { id: 41, question: "Предпочитаете ли вы больше строить планы, чем действовать?" },
    { id: 42, question: "Откладываете ли вы иногда на завтра то, что должны сделать сегодня?" },
    { id: 43, question: "Нервничаете ли вы в местах, подобных лифту, метро, туннелю?" },
    { id: 44, question: "При знакомстве вы обычно первыми проявляете инициативу?" },
    { id: 45, question: "Бывают ли у вас сильные головные боли?" },
    { id: 46, question: "Считаете ли вы обычно, что все само собой уладится и придет в норму?" },
    { id: 47, question: "Трудно ли вам заснуть ночью?" },
    { id: 48, question: "Лгали ли вы когда-нибудь в своей жизни?" },
    { id: 49, question: "Говорите ли вы иногда первое, что придет в голову?" },
    { id: 50, question: "Долго ли вы переживаете после случившегося конфуза?" },
    { id: 51, question: "Замкнуты ли вы обычно со всеми, кроме близких друзей?" },
    { id: 52, question: "Часто ли с вами случаются неприятности?" },
    { id: 53, question: "Любите ли вы рассказывать истории друзьям?" },
    { id: 54, question: "Предпочитаете ли вы больше выигрывать, чем проигрывать?" },
    { id: 55, question: "Часто ли вы чувствуете себя неловко в обществе людей выше вас по положению?" },
    { id: 56, question: "Когда обстоятельства против вас, обычно вы думаете тем не менее, что стоит еще что-либо предпринять?" },
    { id: 57, question: "Часто ли у вас сосет под ложечкой перед важным делом?" },
];

var currentQuestion = -1;
var canClick = false;
var askTime;

var smallFont = {
    family: 'Georgia',
    size: 24,
    anchor: 'middle',
    leading: 1.3,
};

var font = {
    family: 'Georgia',
    size: 48,
    anchor: 'middle',
    leading: 1.3,
};

var questionText = draw.text("")
    .move('50%', '50%')
    .size('80%', '40%')
    .font(font);

var statusText = draw.plain("")
    .move('50%', '10%')
    .font(smallFont);

var noText = draw.plain("Нет")
    .font(font)
    .move("35%", "90%")
    .style('cursor', 'pointer')
    .click(function(){ click(false); });

var yesText = draw.plain("Да")
    .font(font)
    .move("65%", "90%")
    .style('cursor', 'pointer')
    .click(function(){ click(true); });

function click(yes) {
    if(!canClick)
        return;

    var data = {
        answer: yes ? 'yes' : 'no',
        question: questions[currentQuestion],
        answerTime: test.getTime() - askTime
    };
    test.log("answer", data);


    canClick = false;
    showNextQuestion();
}

function showNextQuestion() {
    currentQuestion++;
    if(currentQuestion >= questions.length) {
        test.complete();
        return;
    }
    questionText.clear();

    var q = questions[currentQuestion];
    test.log("asked", q);
    askTime = test.getTime();

    statusText.plain("Вопрос " + q.id + " / " + questions.length);

    let lines = splitWords(questions[currentQuestion].question, splitBy);
    questionText.text(function(add) {
        lines.forEach(function(line) {
            add.tspan(line).newLine();
        });
    });
    questionText.y(draw.viewbox().height * 0.45 - questionText.bbox().height * 0.5);

    canClick = true;
}

test.on("start", function() {
    showNextQuestion();
});

function splitWords(str, rowLen) {
    var res = [str];
    var lastSpace = -1;
    var rowi = 0;
    for (var i = 0; i < str.length; i++) {
        if(str[i] === ' ')
            lastSpace = rowi;

        if(rowi > rowLen && lastSpace > -1) {
            var last = res[res.length - 1];
            res[res.length - 1] = last.substring(0,lastSpace);
            res.push(last.substring(lastSpace + 1));
            rowi = rowLen - lastSpace;
            lastSpace = -1;
        }

        rowi++;
    }

    return res;
}