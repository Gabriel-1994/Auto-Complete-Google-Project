from model import t

def suggestionsRec(node, word, key):
    if node["last"]:
        t.word_list.append([word])
        t.word_list.append(node["obj"].get("sentence"))
        t.word_list.append([node["obj"].get("source_text")])
        t.word_list.append(node["obj"].get("offset"))
        t.word_list.append([get_score(word, key)])

    for a, n in node["children"].items():
        suggestionsRec(n, word + a, key)


def findSuggestionForTwoPlusWords(key, point):
    output = []
    mylis = key.split(" ")
    result = []

    result = printAutoSuggestions(mylis[0], 0)
    for i in range(0, len(result), 5):
        sentences = result[i + 1]
        for sentence in sentences:
            flag = 0
            sentence = sentence.split(" ")
            try:
                index = sentence.index(mylis[0])
            except:
                flag = 1
            if flag == 0:
                for j in range(1, len(mylis)):
                    if index+j >= len(sentence):
                        break
                    if mylis[j] not in sentence[index + j]:
                        break
                else:
                    output.append(sentence[index:index+len(mylis)])  # the word/s that we guessed
                    output.append(" ".join(sentence))  # sentence
                    output.append(result[i + 2])  # filename
                    output.append([index])
                    temp_str = sentence[index + 1]
                    output.append([get_score(mylis[0]+" "+temp_str, key)])

    if point == 0:
        output = mySorts(output, 0)
    else:
        output = mySorts(output, 0)

    return output

# function only takes 1 word or less
def printAutoSuggestions(key, flag):
    t.word_list = []
    node = t.root
    not_found = False
    temp_word = ''
    for a in list(key):
        if not node["children"].get(a):
            not_found = True
            break
        temp_word += a
        node = node["children"][a]
    if not_found:
        return 0
    suggestionsRec(node, temp_word, key)
    result = list(t.word_list)
    if flag == 1:
        result = mySorts(result, 1)

    return result

def get_score(word, key):
    score = 0
    #when both are qual
    if len(word) == len(key):
        return int(len(key)*2)
    #when adding to key
    elif len(word) > len(key):
        score += len(key)*2
        for i in range(len(key),len(word)):
            if i == 0:
                score -= 10
            if i == 1:
                score -= 8
            if i == 2:
                score -= 6
            if i == 3:
                score -= 4
            if i >= 4:
                score -= 2
        return score


def mySorts(results, flag):
    scoreList = []
    newResult = []
    for k in range(0,int(len(results)/5),5):
        scoreList.append(results[k+4][0])
    scoreList.sort(reverse=True)
    scoreList = scoreList[0:5]

    j = 0
    i = 0
    while j < int(len(results)/5) and i < len(scoreList):
        if scoreList[i] == results[j + 4][0]:
            if flag == 0:
                results[j + 1] = [[results[j + 1]]]
            else:
                results[j + 1] = [results[j + 1]]
            newResult.append(results[j:j + 5])
            i += 1
        j += 5

    return newResult



#fix score
def delete_letter(key, oneword, flag):
    #this iy
    if not oneword:
       result = findSuggestionForTwoPlusWords(key[0:flag], 0)
       if result:
            return result
       else:
           flag -= 1
           return delete_letter(key, oneword, flag)

    else:
        result = printAutoSuggestions(key[0:flag], 1)
        if result:
            return result
        else:
            flag -= 1
            return delete_letter(key, oneword, flag)
#thqs
def add_letter(key,oneword):
    vowels = ["a", "o", "e", "i", "u"]
    temp_key = key
    i = 0
    j = len(key)-1
    max_score = -100
    new_result = []
    result = []

    if not oneword:
        while i < len(vowels) and j >= 0:
            key = key[:j] + vowels[i] + key[j+1:]

            result = findSuggestionForTwoPlusWords(key, 1)
            if result:
                if type(result[0][4][0]) == int:
                    if result[0][4][0] > max_score:
                        max_score = result[0][4][0]
                        new_result = result

                if i == 4 and max_score != -100:
                    return new_result
                if i == 4 and max_score == -100:
                    i = 0
                    j -= 1
                    key = temp_key
                i += 1

            else:
                if i == 4 and max_score != -100:
                    return new_result
                if i == 4 and max_score == -100:
                    i = 0
                    j -= 1
                    key = temp_key
                i += 1
    else:
        while i < len(vowels) and j >= 0:
            key = key[:j] + vowels[i] + key[j+1:]
            result = printAutoSuggestions(key, 0)
            if result:
                result = mySorts(result, 1)
                if type(result[0][4][0]) == int:
                    if result[0][4][0] > max_score:
                        max_score = result[0][4][0]
                        new_result = result

                if i == 4 and max_score != -100:
                    return new_result
                if i == 4 and max_score == -100:
                    i = 0
                    j -= 1
                    key = temp_key
                i += 1

            else:
                if i == 4 and max_score != -100:
                    return new_result
                if i == 4 and max_score == -100:
                    i = 0
                    j -= 1
                    key = temp_key
                i += 1
