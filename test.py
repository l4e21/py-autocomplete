class Trie():

    # todo, create a data structure so I can write actual words and it creates this dict for me automatically
    # Should I store this within a DB?
    # what about capitalisation?
    # can I implement this into emacs or the shell? Better to write this in C probably...

    autocompletion_graph = {
        "a": {"weight": 1,
              "a": {"weight": 1000},
              "n": {"weight": 5,
                    "t": {"weight": 3,
                          "word": True,
                          "i": {"weight": 4,
                                "b": {"weight": 4,
                                      "o": {"weight": 3,
                                            "d": {"weight": 3,
                                                  "y": {"weight": 2,
                                                        "word": True}}}},
                                "g": {"weight": 6,
                                      "o": {"weight": 2,
                                            "n": {"weight": 3,
                                                  "e": {"weight": 1,
                                                        "word": True}}}}}}}},
        "b": {"weight": 1,
              "a": {"weight": 30}},
        "c": {"weight": 1,
              "a": {"weight": 30,
                    "a": {"weight": 50},
                    "t": {"weight": 2}}},
        "d": {"weight": 1,
              "a": {"weight": 30},
              "e": {"weight": 10,
                    "m": {"weight": 10,
                          "o": {"weight": 5,
                                "word": True,
                                "n": {"weight": 3,
                                      "word": True}}}}},
        "h": {"weight": 1,
              "a": {"weight": 30},
              "e": {"weight": 29,
                    "l": {"weight": 5,
                          "l": {"weight": 5,
                                "o": {"weight": 5,
                                      "word": True},
                                "p": {"weight": 500},
                                "a": {"weight": 3,
                                      "s": {"weight": 3,
                                            "word": True}}}}}},
        "r": {"weight": 1,
              "e": {"weight": 1,
                    "x": {"weight": 6,
                          "word": True}}},
        "w": {"weight": 1,
              "r": {"weight": 4,
                    "o": {"weight": 6,
                          "n": {"weight": 3,
                                "g": {"weight": 1,
                                      "word": True}}}}}
    }

    def __init__(self, _string, history=[]):
        self.current_node = _string[0]
        self.history = history + [self.current_node]

        if len(_string) > 1:
            self.child = Trie(_string[1:], self.history)


def completion_algo(graph, travel_dist=0):
    current_candidate = ""
    current_weight = 99999
    keys = list(graph.keys())

    for key in keys:
        if len(list(graph[key].keys())) > 1 and not graph[key].get("word", False):
            travel_dist = graph[key].pop("weight")

            graph[key].pop("word", None)

            (adjusted_candidate, adjusted_weight) = completion_algo(graph=graph[key],
                                                                    travel_dist=travel_dist)
            if adjusted_weight < current_weight:
                current_weight = adjusted_weight
                current_candidate = key + adjusted_candidate

        else:
            if graph[key]["weight"] + travel_dist < current_weight:
                current_weight = graph[key]["weight"] + travel_dist
                current_candidate = key

    return (current_candidate, current_weight)


def autocomplete(_string):
    _string = [s for s in _string]
    tree = Trie(_string)

    while True:
        try:
            tree = tree.child
        except:
            break

    graph = tree.autocompletion_graph

    for letter in tree.history:
        graph = graph[letter]

    graph.pop("weight")
    graph.pop("word", None)

    return "".join(_string) + completion_algo(graph)[0]


print(autocomplete("dem"))  # demo
print(autocomplete("ca"))  # cat
print(autocomplete("hell"))  # hello
print(autocomplete("wron"))  # wrong
print(autocomplete("anti"))  # antigone
print(autocomplete("re"))  # rex
