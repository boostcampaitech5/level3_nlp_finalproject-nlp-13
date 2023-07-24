var word1 = document.getElementById("word_box1").innerText
var word2 = document.getElementById("word_box2").innerText
var word3 = document.getElementById("word_box3").innerText


function word1_click(){
    var f = document.createElement("form");
    f.setAttribute("method","post");
    f.setAttribute("action","word_learning");
    
    var hiddenField = document.createElement('input');
    hiddenField.setAttribute('type','hidden');
    hiddenField.setAttribute('name','word');
    hiddenField.setAttribute('value',word1);
    f.appendChild(hiddenField);

    document.body.appendChild(f);
    f.submit();
}

function word2_click(){
    var f = document.createElement("form");
    f.setAttribute("method","post");
    f.setAttribute("action","word_learning");
    
    var hiddenField = document.createElement('input');
    hiddenField.setAttribute('type','hidden');
    hiddenField.setAttribute('name','word');
    hiddenField.setAttribute('value',word2);
    f.appendChild(hiddenField);

    document.body.appendChild(f);
    f.submit();
}

function word3_click(){
    var f = document.createElement("form");
    f.setAttribute("method","post");
    f.setAttribute("action","word_learning");
    
    var hiddenField = document.createElement('input');
    hiddenField.setAttribute('type','hidden');
    hiddenField.setAttribute('name','word');
    hiddenField.setAttribute('value',word3);
    f.appendChild(hiddenField);

    document.body.appendChild(f);
    f.submit();
}