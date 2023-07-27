import pymongo
import random
import yaml

with open('./flask/api.yaml') as f:
    api = yaml.load(f, Loader=yaml.FullLoader)

client = api['client']
connection = pymongo.MongoClient(client)
db = connection.data
word = db.words

rules = ['', '18항', '12.1항', '30.3항', '17.1항', '19.1항', '17항', '20항', '10항', '15항', '30.1항', '13항', '12.3.1항', '5.4항', '24항', '9항', '19항', '25항', '23항', '26항', '14항', '5.3항', '12.1.2항', '11항', '29항', '12.1.1항', '28항']

def random_recommend(input, count):
    """
    input에서 count만큼 랜덤으로 추출하는 함수
    """
    if len(input) <= count:
        return input
    return random.sample(input, count)

def word_recommend(input):
    """
    3개의 단어 추천해주는 함수
    """
    recommend = random_recommend(input, 3)
    # 해당 규칙이 적용된 단어가 3개 이하이면 랜덤으로 다른 규칙에서 단어 추출
    if len(recommend) != 3:
        a = random.choice(rules)
        d = rule_data(a)
        recommend2 = random_recommend(d, 3-len(recommend))
        recommend += recommend2
    recommend_word = []
    for r in recommend:
        recommend_word.append(r['word'])
    return recommend_word

def rule_data(rule):
    """
    input으로 받은 규칙과 동일한 데이터 리스트로 반환하는 함수
    """
    if rule == '': 
        query = {'rule': []}
        search = word.find(query)
        data = list(search)
    else:
        query = {'rule' : rule}
        search = word.find(query)
        data = list(search)
    return data

def today_words():
    """
    오늘의 단어 3개 리스트로 반환하는 함수
    """
    three_rules = random.sample(rules, 3)
    
    words = []
    
    for rule in three_rules:
        data = rule_data(rule)
        random_data = random.choice(data)
        words.append(random_data['word'])
    
    return words

def word_dict(input_word):
    """
    입력으로 들어온 단어의 정보 딕셔너리로 반환하는 함수
    단어에 적용된 규칙이 여러 개일 경우 랜덤으로 하나를 골라 추천 단어를 만듭니다.
    """
    query = {'word': input_word}
    search = word.find(query)
    data = list(search)[0]
    rule = data['rule']
    if len(rule) > 1:
        rule = random.choice(rule)
    elif len(rule) == 1:
        rule = rule[0]
    rule_list = rule_data(rule)
    rule_list.remove(data)
    recommend_word = word_recommend(rule_list)
    index_ = data['index']
    word_ = data['word']
    meaning = data['mean']
    audio_path = f'../static/src/audio/nara/{index_}_{word_}_nara.wav'
    if rule == []: rule = ''
    a = {'word':word_, 'g2p_word':data['g2p_word'], 'meaning': meaning, 'rule': rule, 'audio': audio_path, 'recommend':recommend_word}
    return a
    
def get_rule_id2text():
    """
    표준발음법 규칙을 딕셔너리 형태로 만드는 함수
    """
    rules = open('./utils/rules.txt', 'r', encoding='utf8').read().strip().split("\n\n")
    rule_id2text = dict()
    for rule in rules:
        rule_id, texts = rule.splitlines()[0], rule.splitlines()[1:]
        rule_id2text[rule_id.strip()] = "\n".join(texts)
    return rule_id2text
    
def get_rule(rule):
    """
    규칙을 입력하면 규칙에 대한 설명을 반환하는 함수
    """
    if rule == '':
        # 적용된 규칙이 없으면 None을 반환합니다.
        return None
    else:
        rule_dict = get_rule_id2text()
        return rule_dict[rule]

if __name__ == '__main__':
    a = today_words()
    print(a)
    for i in a:
        b = word_dict(i)
        print(b)
        print(get_rule(b['rule']))
