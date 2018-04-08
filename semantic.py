from pymongo import MongoClient
import numpy as np
import math
import config 

# mongoClient = MongoClient(config.mongo.host, 27017)
uri = 'mongodb://%s:%s@%s:%s/%s' % (config.username, config.password, config.host, config.port, config.db)
db = MongoClient(uri).get_database()
print(db)
corpusCollection = db.Corpus

dictionary =[]
scoreOfWord = {}

def init():
    corpus = corpusCollection.find()
    for term in corpus:
    	dictionary.append(term["content"])
    	scoreOfWord[term["content"]] = term["weight"]

def WordOfText(s):
    s = s.strip().lower()
    s = s.replace(',', ' ')
    s = s.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
    s = ' '.join(s.split())
    return s.split(' ')

def extract(text):
    Terms = []
    EmotionalValues = []
    w = WordOfText(text)
    start = 0
    stop = len(w)
    isStop = False
    while (isStop == False and stop >= 0):
        term = preFix = ""
        for index in range(start, stop):
            term += w[index] + " "
        for index in range(0, start):
            preFix += w[index] + " "
            
        term = term.strip()  
        preFix = preFix.strip()
        
        if (term in dictionary):
            Terms.append(term)
            EmotionalValues.append(scoreOfWord[term])
            if (start == 0):
                isStop = True
            else:
                stop = start
                start = 0

        else: 
            if (start == stop):
                stop -= 1
                start = 0
            else:
                start += 1
    return [EmotionalValues, Terms]  


def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def semanticAnalysisExecute(sentence):
#   sentence= """Chưa được trải nghiệm thực tế nhưng lướt qua dàn cấu hình thì thấy Prime X max 2018 này khá ngon so với các dòng điện thoại khác cùng phân khúc. 1 là 4 cam độ phân giải cao, tích hợp đầy đủ xóa phông, selfie góc rộng. 2 là pin trâu. 3 là giao diện đẹp. 4 là giá hợp lý"""
    res = extract(sentence)
    
    G = np.array(res[0])
    P = (G>0) * G
    N = (G<0) * G

    if (np.count_nonzero(G) == 0):
        return sentence + " -> là câu chưa biết"
    elif (np.count_nonzero(P) == 0):
        return sentence + " -> là câu chê"
    elif (np.count_nonzero(N) == 0):
        return sentence + " -> là câu khen"
    else:  
        positiveCos = cosine_similarity(P, G)
        negativeCos = cosine_similarity(N, G)
        if positiveCos > negativeCos:
            return sentence + " -> là câu khen"
        else:
            return sentence + " -> là câu chê"
