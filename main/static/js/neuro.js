let question, theme, questionsCount;
let current = 0;
let answers = [];
let score = 0;

async function getQuestion(theme){
    let res = await fetch(`/neuro/${theme}`);
    if(res.ok){
        let result;
        try{
            result = await res.json();
        }
        catch{
            alert("Неудачный ответ нейросети... Генерирую заново");
            return false;
        }
        return result;
    }
    alert("Неудачный ответ нейросети... Генерирую заново");
    return false;
}

function renderResult(){
    document.querySelector(".title").innerText = "Итог";
    document.querySelector(".answers").innerHTML = `<div class="result"><p>Вы набрали ${score}/${questionsCount} баллов</p><a href="../../" class="gohome">На главную</a></div>`;
}

function nextQuestion(){
    if(current === 0){
        const nTitle = document.querySelector("#neuro-title").value;
        const nCount = document.querySelector("#neuro-count").value;
        if(nTitle.length > 0 && nCount.length > 0){
            questionsCount = Number(nCount);
            theme = nTitle;
            console.log("Вход", nTitle, nCount);
            getQuestion(nTitle).then((data) => {
                if(data){
                    current++;
                    question = data;
                    renderQuestion(data);
                }
                else{
                    nextQuestion()
                }
            })
        }
    }
    else if(current <= questionsCount){
        let corrects = question.answers
        .map((ans, i) => (ans.correct) ? i : null)
        .filter(ans => ans != null).sort();
        console.log(corrects, answers.sort());
        if(corrects.toString() === answers.sort().toString() ){
            score++;
        }
        answers = [];
        if(current >= questionsCount){
            renderResult();
        }
        else{
            getQuestion(theme).then((data) => {
                if(data){
                    current++;
                    question = data;
                    renderQuestion(data);
                }
                else{
                    nextQuestion()
                }
            })
        }
    }
}

function answerQuestion(e){
    e.target.classList.toggle("selected");
    let answer = Number(e.target.id.match(/\d+/));
    if(e.target.classList.contains("selected")){
        answers.push(answer);
    }
    else{
        answers.splice(answers.indexOf(answer), 1);
    }
}

function renderQuestion(){
    document.querySelector(".title").innerText = `(${current} / ${questionsCount}) ${question.text}`;
    let answers = question.answers.map((answer, i) => `<button class="answer" id="answer${i}">${answer.text}</button>`).join("\n");
    document.querySelector(".answers").innerHTML = answers;
    document.querySelectorAll(".answer").forEach(el => {
        el.addEventListener("click", answerQuestion)
    })
}

document.querySelector(".next").addEventListener("click", nextQuestion);