const $audioE = document.querySelector("audio");
const $btn = document.getElementById("record");
var word1 = document.getElementById("word1");
var word2 = document.getElementById("word2");
var word3 = document.getElementById("word3");
var add_or_today = document.getElementById("add_or_today").innerText;

let isRecording = false;
let mediaRecorder = null;

const audioArray = [];

$audioE.src=document.getElementById("user_audio").innerText

function play(){
    var audio = new Audio(document.getElementById('audio').innerText);
    audio.loop = false;
    audio.volume = 0.3;
    audio.play();
}

$btn.onclick = async function(event){
    if (!isRecording){
        isRecording = true;
        document.getElementById('record_button').src="../static/src/img/record_clicked.png";
        const mediaStream = await navigator.mediaDevices.getUserMedia({audio: true});
        mediaRecorder = new MediaRecorder(mediaStream);

        mediaRecorder.ondataavailable = (event)=>{
            audioArray.push(event.data);
        }

        mediaRecorder.onstop = (event)=>{
            const blob = new Blob(audioArray, {"type": "audio/wav"});
            
            audioArray.splice(0);
            
            var data=new FormData()
            data.append('file', blob, 'audio.wav')

            fetch('http://127.0.0.1:40001/get_user_pronounce',{
                method: 'POST',
                body: data
            }).then(response => response.json()
            )

            var f = document.createElement("form");
            f.setAttribute("method","post");
            f.setAttribute("action","get_user_pronounce");

            document.body.appendChild(f);
            f.submit();
        }
        mediaRecorder.start();
        
    }else{
        document.getElementById('record_button').src="../static/src/img/record.png";
        mediaRecorder.stop();
        isRecording = false;
    }
}

function word1_click(){
    var f = document.createElement("form");
    f.setAttribute("method","post");
    if (add_or_today=='today'){
        f.setAttribute("action","word_learning_additional_word");
    }
    else{
        f.setAttribute("action","word_learning_todays_word");
    }    
    
    var num = document.createElement('input');
    num.setAttribute('type','hidden');
    num.setAttribute('name','num');
    num.setAttribute('value',0);
    f.appendChild(num);

    var word = document.createElement('input');
    word.setAttribute('type','hidden');
    word.setAttribute('name','word');
    word.setAttribute('value',word1.innerText);
    f.appendChild(word);

    document.body.appendChild(f);
    f.submit();
}

function word2_click(){
    var f = document.createElement("form");
    f.setAttribute("method","post");
    if (add_or_today=='today'){
        f.setAttribute("action","word_learning_additional_word");
    }
    else{
        f.setAttribute("action","word_learning_todays_word");
    }    
    
    var num = document.createElement('input');
    num.setAttribute('type','hidden');
    num.setAttribute('name','num');
    num.setAttribute('value',1);
    f.appendChild(num);

    var word = document.createElement('input');
    word.setAttribute('type','hidden');
    word.setAttribute('name','word');
    word.setAttribute('value',word2.innerText);
    f.appendChild(word);

    document.body.appendChild(f);
    f.submit();
}

function word3_click(){
    var f = document.createElement("form");
    f.setAttribute("method","post");
    if (add_or_today=='today'){
        f.setAttribute("action","word_learning_additional_word");
    }
    else{
        f.setAttribute("action","word_learning_todays_word");
    }    
    
    var num = document.createElement('input');
    num.setAttribute('type','hidden');
    num.setAttribute('name','num');
    num.setAttribute('value',2);
    f.appendChild(num);

    var word = document.createElement('input');
    word.setAttribute('type','hidden');
    word.setAttribute('name','word');
    word.setAttribute('value',word3.innerText);
    f.appendChild(word);

    document.body.appendChild(f);
    f.submit();
}