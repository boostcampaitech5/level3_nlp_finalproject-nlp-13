from g2pk import G2p
from tqdm.auto import tqdm

def gtop(sents : list):
    """
    desc : 문장 리스트를 넣으면 리스트 내의 각 문장에 g2p를 적용시킨 후 리스트 반환
    input : list type
    output : list type
    requirements : pip install g2pk, pip install tqdm
    """
    result = []
    g2p = G2p()
    for sent in tqdm(sents, desc="발음으로 변경중"):
        result.append(g2p(sent, group_vowels=True, descriptive=True))

    return result
