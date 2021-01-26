import os
import json
import pickle


class AutoCompleteData():
    def __init__(self):
        self.sentence = []
        self.source_text = ""
        self.offset = []
        self.score = 0

class TrieNode():
    def __init__(self):
        self.children = {}
        self.last = False
        # Only on nodes that makeup a word we have all the attributes of autocompletedata
        self.obj = AutoCompleteData()

class Trie():
    def __init__(self):
        self.sorted = False
        self.root = TrieNode()
        self.word_list = []

    def formTrie(self, keys):
        for i in range(0, len(keys) - 1, 3):
            self.insert(keys[i], keys[i + 1], keys[i + 2])

    def insert(self, key, sentences, filename):
        node = self.root
        for a in list(key):
            if not node.children.get(a):
                node.children[a] = TrieNode()
            node = node.children[a]
        node.last = True
        self.getOffset(node, sentences, key)
        node.obj.sentence.append(" ".join(sentences))
        node.obj.source_text = filename

    def getOffset(self, node, sentence, word):
        sentence = " ".join(sentence)
        sentence = sentence.lower()
        node.obj.offset.append(sentence.find(word))

    def search(self, key):
        node = self.root
        found = True
        for a in list(key):
            if not node.children.get(a):
                found = False
                break
            node = node.children[a]
        return node and node.last and found
    """
    def save_to_json(self, file_name):
        json_data = json.dumps(self.root,default=lambda x: x.__dict__)
        f = open(file_name + ".json", "w")
        f.write(json_data)
        f.close()
    def load_from_json(self, file_name):
        json_file = open(file_name, "r")
        self.root = json.load(json_file)
        #self.root = self.root["children"]
        json_file.close()
    """
    def save_to_pickle(self, file_name):
        json_data = json.dumps(self.root, default=lambda x: x.__dict__)
        f = open(file_name + ".pkl", "wb")
        pickle.dump(json_data, f)
        f.close()

    def load_from_pickle(self, file_name):
        f = open(file_name + ".pkl", "rb")
        self.root = pickle.load(f)
        self.root = json.loads(self.root)
        f.close()

def load_data():
    allfiles = get_files_path("Model")
    biglis=[]
    for filename in allfiles:
        print(filename)
        if filename.endswith(".txt"):
            with open(filename, encoding="utf8") as f:
                mylis = []
                for row in f:
                    row = ExtractAlphanumeric(row)
                    mylis = row.split()
                    for i in mylis:
                        i = i.lower()
                        biglis.append(i)
                        biglis.append(mylis)
                        biglis.append(filename)
    return biglis

def get_files_path(diricory_path):
    txt_file = []
    dir_file = []
    for path in os.listdir(diricory_path):
        full_path = os.path.join(diricory_path, path)
        if os.path.isfile(full_path):
            txt_file.append(full_path)
        elif os.path.isdir(os.path.join(diricory_path,path)):
            dir_file.append(os.path.join(diricory_path, path))
    if len(dir_file) == 0:
        return txt_file
    else:
        for dirictory in dir_file:
            txt = get_files_path(dirictory)
            txt_file += txt
    return txt_file

def ExtractAlphanumeric(InputString):
    from string import ascii_letters, digits
    return "".join([ch for ch in InputString if (ch in (ascii_letters + digits)) or ch == " "])


t = Trie()
#t.formTrie(load_data())
#t.save_to_pickle("data")
t.load_from_pickle("data")
