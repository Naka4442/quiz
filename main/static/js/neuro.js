let questions;
let current = 0;

async function getQuestion(theme){
    let res = await fetch(`/neuro/${theme}`);
    let result = await res.json();
    return result;
}

function nextQuestion(){
    if(current === 0){
        const nTitle = document.querySelector("#neuro-title").value;
        const nCount = document.querySelector("#neuro-count").value;
        if(nTitle.length > 0 && nCount.length > 0){
            console.log("Вход", nTitle, nCount);
            getQuestion(nTitle).then((data) => {
                console.log(data);
            })
        }
    }
}


document.querySelector(".next").addEventListener("click", nextQuestion);