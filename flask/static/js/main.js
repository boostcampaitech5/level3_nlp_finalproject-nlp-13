function word1_click(){
    var f = document.createElement("form");
    f.setAttribute("method","post");
    f.setAttribute("action","word_learning_todays_word");
    
    var hiddenField = document.createElement('input');
    hiddenField.setAttribute('type','hidden');
    hiddenField.setAttribute('name','num');
    hiddenField.setAttribute('value',0);
    f.appendChild(hiddenField);

    document.body.appendChild(f);
    f.submit();
}

function word2_click(){
    var f = document.createElement("form");
    f.setAttribute("method","post");
    f.setAttribute("action","word_learning_todays_word");
    
    var hiddenField = document.createElement('input');
    hiddenField.setAttribute('type','hidden');
    hiddenField.setAttribute('name','num');
    hiddenField.setAttribute('value',1);
    f.appendChild(hiddenField);

    document.body.appendChild(f);
    f.submit();
}

function word3_click(){
    var f = document.createElement("form");
    f.setAttribute("method","post");
    f.setAttribute("action","word_learning_todays_word");
    
    var hiddenField = document.createElement('input');
    hiddenField.setAttribute('type','hidden');
    hiddenField.setAttribute('name','num');
    hiddenField.setAttribute('value',2);
    f.appendChild(hiddenField);

    document.body.appendChild(f);
    f.submit();
}