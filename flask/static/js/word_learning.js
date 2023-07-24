const $audioE = document.querySelector("audio");
const $btn = document.getElementById("record")

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
