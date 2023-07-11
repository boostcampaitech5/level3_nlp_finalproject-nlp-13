def compare(sen1,sen2):
    """
    사용자의 발음과 기존 발음을 비교하는 함수 
    띄어쓰기 기준으로 각 발음 비교한다. 
    sen1 : 사용자 발화 문장
    sen2 : 기존 문장
    """
    nSen1 = sen1.split()
    nSen2 = sen2.split()

    diff = []
    for i in range(0,len(nSen1)):
        if nSen1[i]!=nSen2[i]:
            diff.append([nSen2[i],nSen1[i]])

    #틀린 부분 출력
    print(diff)


if __name__=="__main__":
    compare("오느른 날씨가 막따","오느른 날씨가 말다.")