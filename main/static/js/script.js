async function getQuestions(id){
    let res = await fetch(`/questions/${id}`);
    let result = await res.json();
    return result;
}

async function complete(id, score){
    const csrftoken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    let res = await fetch(`/complete/${id}`, {
        method : "POST",
        body : JSON.stringify({score}),
        headers: { "X-CSRFToken": csrftoken }
    });
    let result = await res.json();
    if(result.result){
        alert("Результаты записаны");
    }
}

let questions;
let current = 0;
let answers = []; 
let quiz_id = Number(document.querySelector("#id").innerText);
let score = 0;

function nextQuestion(){
    if(questions[current].kind == "TF"){
        let correct = questions[current].correct;
        if(correct === answers) score++;
    }
    else if(questions[current].kind == "WV"){
        let corrects = questions[current].answers
            .map((ans, i) => (ans.correct) ? i : null)
            .filter(ans => ans != null).sort();
        console.log(corrects, answers.sort());
        if(corrects.toString() === answers.sort().toString() ){
            score++;
        }
    }
    console.log(`Счёт ${score}`)
    current++;
    answers = [];
    if(current < questions.length){
        renderQuestion();
    }
    else{
        renderResult();
    }
}

function answerQuestion(e){
    if(questions[current].kind = "TF"){
        let answer = document.querySelector(".tf").value;
        answers = answer;
    }
    else if(questions[current].kind = "WV"){
        e.target.classList.toggle("selected");
        let answer = Number(e.target.id.match(/\d+/));
        if(e.target.classList.contains("selected")){
            answers.push(answer);
        }
        else{
            answers.splice(answers.indexOf(answer), 1);
        }
    }
}

function renderResult(){
    complete(quiz_id, score).then(answer => console.log(answer));
    document.querySelector(".title").innerText = "Итог";
    document.querySelector(".answers").innerHTML = `<div class="result"><p>Вы набрали ${score}/${questions.length} баллов</p><a href="../../" class="gohome">На главную</a><a href="../../rating/${quiz_id}" class="gohome">Рейтинг</a></div>`;
}

function renderQuestion(){
    document.querySelector(".title").innerText = questions[current].text;
    if(questions[current].kind === "TF"){
        document.querySelector(".answers").innerHTML = `<input type="text" placeholder="Ответ" class="tf">`;
        document.querySelector(".tf").addEventListener("input", answerQuestion);
    }
    else if(questions[current].kind === "WV"){
        let answers = questions[current].answers.map((answer, i) => `<button class="answer" id="answer${i}">${answer.text}</button>`).join("\n");
        document.querySelector(".answers").innerHTML = answers;
        document.querySelectorAll(".answer").forEach(el => {
            el.addEventListener("click", answerQuestion)
        })
    }
}

document.querySelector(".next").addEventListener("click", nextQuestion);

getQuestions(quiz_id).then(data => {
    questions = data;
    console.log(questions);
    renderQuestion()
});

