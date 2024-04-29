let isAdddingAnswer = false;
let isEditingQuestion = false;
document.querySelector(".add-question").addEventListener("click", e => {
    document.querySelector(".question-cards").insertAdjacentHTML("beforeend", 
    `<div class="question">
        <p>
            <input type="text" placeholder="Текст вопроса" class="question-title">
            <select class="question-kind">
                <option value="WV" selected>С вариантами ответа</option>
                <option value="TF">Поле ввода</option>
            </select>
            <button class="end-adding">✓</button>
        </p>
    </div>`);
    document.querySelectorAll(".end-adding").forEach(el => el.addEventListener("click", e => {
        let title = e.target.parentElement.querySelector(".question-title").value;
        let kind =  e.target.parentElement.querySelector(".question-kind").value;
        addQuestion(title, kind).then(data => {
            if(data){
                alert("Вопрос добавлен");
                window.location.reload();
            }
            else{
                alert("Ошибка")
            }
        })
    }))
});

document.querySelectorAll(".answer").forEach(el => el.addEventListener("click", (e) => {
    e.target.parentElement.querySelectorAll(".answer").forEach(el => el.classList.remove("correct-answer"));
    //e.target.classList.add("correct-answer")//Добавление класса
    correctAnswer(e.target.querySelector(".aid").value).then(data => {
        if(data){
            alert("Ответ изменен");
            window.location.reload();
        }
        else{
            alert("Ошибка")
        }
    })
}))

document.querySelectorAll(".qtitle").forEach(el => el.addEventListener("click", (e) => {
    let qid = Number(e.target.parentElement.parentElement.querySelector(".qid").value);
    let title = e.target.innerText;
    e.target.parentElement.innerHTML = `<p>
        <input type="text" placeholder="Текст вопроса" class="question-title" value="${title}">
        <button class="end-editing">✓</button>
    </p>`;
    document.querySelectorAll(".end-editing").forEach(el => el.addEventListener("click", e => {
        let title = e.target.parentElement.querySelector(".question-title").value;
        editQuestion(qid, title).then(data => {
            if(data){
                alert("Вопрос изменен");
                window.location.reload();
            }
            else{
                alert("Ошибка")
            }
        })
        console.log("В будущем я изменю вопрос", qid);
    }))
}))

document.querySelectorAll(".add-answer").forEach(el => el.addEventListener("click", (e) => {
    if(!isAdddingAnswer){
        isAdddingAnswer = true;
        el.innerHTML = `<input type="text" placeholder="Ответ" class="answer-title">
        <button class="end-adding-answer">✓</button>`;
        document.querySelectorAll(".end-adding-answer").forEach(el => el.addEventListener("click", e => {
            let title = e.target.parentElement.querySelector(".answer-title").value;
            let question = e.target.parentElement.parentElement.parentElement.querySelector(".qid").value;
            console.log(title, question);
            addAnswer(title, question).then(data => {
                if(data){
                    alert("Ответ добавлен");
                    window.location.reload();
                }
                else{
                    alert("Ошибка")
                }
            })
        }))
    }
}))

document.querySelectorAll(".end-adding-correct").forEach(el => el.addEventListener("click", (e) => {
    let title = e.target.parentElement.querySelector(".adding-correct").value;
    let question = e.target.parentElement.parentElement.querySelector(".qid").value;
    console.log(title, question);
    addAnswer(title, question).then(data => {
        if(data){
            alert("Ответ добавлен");
            window.location.reload();
        }
        else{
            alert("Ошибка")
        }
    })
}))

document.querySelectorAll(".qdelete").forEach(el => el.addEventListener("click", (e) => {
    let question = e.target.parentElement.parentElement.querySelector(".qid").value;
    console.log(question);
    deleteQuestion(question).then(data => {
        if(data){
            alert("Вопрос удален");
            window.location.reload();
        }
        else{
            alert("Ошибка")
        }
    })
}))

document.querySelectorAll(".andelete").forEach(el => el.addEventListener("click", (e) => {
    let aid = Number(e.target.parentElement.querySelector(".aid").value);
    deleteAnswer(aid, "WV").then(data => {
        if(data){
            alert("Ответ удален");
            window.location.reload();
        }
        else{
            alert("Ошибка")
        }
    })
}))

document.querySelectorAll(".text-delete").forEach(el => el.addEventListener("click", (e) => {
    let qid = Number(e.target.parentElement.parentElement.querySelector(".qid").value);
    deleteAnswer(qid, "TF").then(data => {
        if(data){
            alert("Ответ удален");
            window.location.reload();
        }
        else{
            alert("Ошибка")
        }
    })
}))

async function addQuestion(title, kind){
    const csrftoken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    let request = await fetch("", {
        method : "POST",
        body : JSON.stringify({title, kind}),
        headers: { "X-CSRFToken": csrftoken }
    })
    let result = await request.json();
    return result.result;
}

async function addAnswer(title, question){
    const csrftoken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    let request = await fetch(`../../add_answer/${question}`, {
        method : "POST",
        body : JSON.stringify({title}),
        headers: { "X-CSRFToken": csrftoken }
    })
    let result = await request.json();
    return result.result;
}

async function  correctAnswer(id){
    const csrftoken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    let request = await fetch("../../correct_answer/", {
        method : "POST",
        body : JSON.stringify({id}),
        headers: { "X-CSRFToken": csrftoken }
    })
    let result = await request.json();
    return result.result;
}

async function  deleteQuestion(id){
    const csrftoken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    let request = await fetch("../../delete_question/", {
        method : "POST",
        body : JSON.stringify({id}),
        headers: { "X-CSRFToken": csrftoken }
    })
    let result = await request.json();
    return result.result;
}

async function  deleteAnswer(id, mode){
    const csrftoken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    let request = await fetch("../../delete_answer/", {
        method : "POST",
        body : JSON.stringify({id, mode}),
        headers: { "X-CSRFToken": csrftoken }
    })
    let result = await request.json();
    return result.result;
}


async function editQuestion(id, title){
    const csrftoken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    let request = await fetch("../../edit_question/", {
        method : "POST",
        body : JSON.stringify({id, title}),
        headers: { "X-CSRFToken": csrftoken }
    })
    let result = await request.json();
    return result.result;
}