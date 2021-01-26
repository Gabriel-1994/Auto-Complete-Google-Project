import controller
import time


def print_results(results, one_word, key):
    if not results or type(results) == int:
        #deletes last letter/s till results are found
        if one_word:
            print_results(controller.add_letter(key, one_word), one_word, key)
        else:
            print_results(controller.delete_letter(key, one_word, -1), one_word, key)

    else:
        print("User Input: ", key)  # once
        for i in range(0, len(results)):
            #if not one_word:
            #    print("Autocompleted word: ", " ".join(results[i][0])) #remove
            #else:
            #    print("Autocompleted word: ", "".join(results[i][0])) #remove
            print("autocomplete number: ", i+1)
            for j in range((len(results[i][1][0]) % 5)):
                print("Starting at: ", results[i][3][j:j+1])
                print("Autocompleted sentence: ", results[i][1][0][j:j+1])
            print("From text file: ", results[i][2])
            print("Score: ", results[i][4])
            print()

def get_results(key):
    result = []
    start = time.time()
    if len(key.split(" ")) > 1:
        result = controller.findSuggestionForTwoPlusWords(key, 0)
        print_results(result, 0, key)

    else:
        result = controller.printAutoSuggestions(key, 1)
        print_results(result, 1, key)
    end = time.time()
    print("latency: ", end-start)
    print()


def run():
    controller.t.load_from_pickle("data")
    while True:
        print("What are you searching for?")
        user_input = input()
        get_results(user_input)
