# 외국인을 위한 발음 교정 서비스, AI야어여

### HYPE연어
<table>
    <tr height="160px">
        <td align="center" width="150px">
            <a href="https://github.com/Yunhee000"><img height="120px" width="120px" src="https://avatars.githubusercontent.com/Yunhee000"/></a>
            <br/>
            <a href="https://github.com/Yunhee000"><strong>김윤희</strong></a>
            <br />
        </td>
        <td align="center" width="150px">
            <a href="https://github.com/8804who"><img height="120px" width="120px" src="https://avatars.githubusercontent.com/8804who"/></a>
            <br/>
            <a href="https://github.com/8804who"><strong>김주성</strong></a>
            <br />
        </td>
        <td align="center" width="150px">
            <a href="https://github.com/bom1215"><img height="120px" width="120px" src="https://avatars.githubusercontent.com/bom1215"/></a>
            <br/>
            <a href="https://github.com/bom1215"><strong>이준범</strong></a>
            <br />
        </td>
        <td align="center" width="150px">
            <a href="https://github.com/ella0106"><img height="120px" width="120px" src="https://avatars.githubusercontent.com/ella0106"/></a>
            <br/>
            <a href="https://github.com/ella0106"><strong>박지연</strong></a>
            <br />
        </td>
        <td align="center" width="150px">
            <a href="https://github.com/HYOJUNG08"><img height="120px" width="120px" src="https://avatars.githubusercontent.com/HYOJUNG08"/></a>
            <br/>
            <a href="https://github.com/HYOJUNG08"><strong>정효정</strong></a>
            <br />
        </td>
    </tr>
</table>
<br>

| 이름 | 역할 |
| :----: | --- |
| **김윤희** | 모델 성능 실험, 자료 DB 구축 |
| **김주성** | 모델 리서치, 모델 성능 실험, 웹 구현 |
| **이준범** | 데이터 전처리, 모델 성능 실험, 로그인 API 연결 |
| **박지연** | Vocab Adaptation, 모델 성능 실험 |
| **정효정** | 모델 리서치, 모델 성능 실험, 로그인 DB 구축 |

## AI야어여란?

AI야어여는 한국어를 학습하며 발음을 교정할 수 있는 한국어 교육 서비스입니다.    
현재 다양한 경로를 통해 한국어를 공부하고자 하는 사람들이 유입되고 있으나 아직 한국어 온라인 교육 플랫폼이 수요에 부족한 상황입니다.   
더블어 대부분의 온라인 한국어 교육 플랫폼은 영어권 사용자에 맞춰져 있어 비영어권이나 다양한 연령대의 사용자에게는 불편함이 있습니다.   
또한 기존 발음 교정 서비스는 발음을 정확하게 인식하지 못하는 경우가 많았습니다.   
   
그로 인해 저희 HYPE 연어는 기초 한국어를 학습하려는 사용자에게 단어 학습 및 발음 교정 서비스를 제공하는 것을 목표로 AI야어여를 만들게 되었습니다.    
하루에 총 3개의 단어를 학습하여 부담 없이 꾸준하게 학습할 수 있도록 하였습니다.   
   
>[발표 영상](link)   
>[발표 자료](link)   
>[wrapup report](link)   

## AI야어여 기능 살펴보기 
#### 1. 로그인 및 출석 기록 (아래 사진의 우측 부분)
![Alt text](/resources/service1.png)
#### 2. 오늘의 단어 학습 
![Alt text](/resources/service2.png)
#### 3. 한국어 외 영어, 중국어, 일본어, 태국어, 베트남어로 학습 가능 
![Alt text](/resources/service3.png)
#### 4. 발음이 틀리면 해당 단어에 적용된 음운 규칙이 같은 다른 단어 추천
![Alt text](/resources/service.gif)
#### 5. 사용자의 음성을 녹음하여 피드백을 제공해주는 기능 제공
![Alt text](/resources/service_rec.gif)
* * *
## Service Architectecture
![Alt text](/resources/architecture.png)
## Service Flow Chart
![Alt text](/resources/flowchart.png)
* * *
## Data 
모델에 한국인이 한국어를 발음하는 현지 발음을 학습시키기 위해 [AI Hub 자유대화 음성 (일반남녀)](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=109)을 사용하였고, 억양 등 외국인이 한국어를 발음할 때의 특성을 학습시키기 위해 [AI Hub 인공지능 학습을 위한 외국인 한국어 발화 음성 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=505)를 사용하였습니다.    
더불어 저희는 발음 나는대로 음성이 텍스트로 변환되길 원했기 때문에 G2P를 이용하여 텍스트를 변환시켰습니다.
![Alt text](/resources/data1.png)
   
이어서 국립국어원에서 제공하는 자주 사용되는 단어 5000여 개를 이용하여 G2P 데이터를 생성하였고, Naver Clover Speech를 이용하여 4명의 음성으로 음성합성하여 새로운 데이터를 추가하였습니다.   
![Alt text](/resources/data2.png)   
## MODEL
외국인 대상 서비스임을 고려해 Cross-Lingual Speech Representation을 학습하는 wav2vec 2.0 기반 XLSR를 사용하였습니다.   

그중 한국어로 발음을 비교하기 때문에 한국어로 pre-training된 모델이 필요하여 huggingface의 [kresnik/wav2vec2-large-xlsr-korean](https://huggingface.co/kresnik/wav2vec2-large-xlsr-korean)를 사용하였습니다. 

총 6가지 실험을 진행하였으며, 한국인 음성 데이터로 학습한 모델, 한국인 음성과 단어 데이터로 학습한 모델, 한국인 음성 데이터와 외국인 발화 데이터로 학습한 모델을 각각 vocab adaptation을 적용 시킨 것과 안한 것으로 나누어 비교하였습니다.      
![Alt text](/resources/model2.png)![Alt text](/resources/model3.png)![Alt text](/resources/model4.png)![Alt text](/resources/model5.png)
   
기존 Tokenzier는 잘 사용되지 않는 꾜, 갇와 같은 문자들은 가지고 있지 않아 unk 토큰으로 처리하는 문제점이 있어 G2P 변환 문장으로 새로운 Vocab을 만들어 해결하였습니다.     
   
<p align="center"><img src="/resources/vocab.png"></img></p>   
<p align="center"><img src="/resources/vocab2.png"></img></p>      


최종적으로 한국인 음성 데이터와 외국인 음성 데이터로 학습 시키고, Vocab Adaptation이 적용되어 있는 모델이 가장 좋은 성능을 보여, 해당 모델을 이용하였습니다. 
![Alt text](/resources/model.png)   
