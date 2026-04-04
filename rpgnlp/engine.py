
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import random
import spacy

_NLP = None
_NLTK_READY = False

def _ensure_nltk_data():
    global _NLTK_READY
    if _NLTK_READY:
        return
    import nltk
    for resource in ('averaged_perceptron_tagger_eng', 'punkt_tab'):
        try:
            nltk.data.find(f'taggers/{resource}' if 'tagger' in resource else f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)
    _NLTK_READY = True

def get_nlp():
    global _NLP
    if _NLP is None:
        try:
            _NLP = spacy.load("en_core_web_md")
        except OSError:
            from spacy.cli import download
            download("en_core_web_md")
            _NLP = spacy.load("en_core_web_md")
    return _NLP

class NLPEngine:
    def __init__(self):
        _ensure_nltk_data()
        self.canon = {
            "attack": [
                "attack", "hit", "strike", "fight", "punch", "slice", "slime", "stab", "slash",
                "shoot", "kick", "bite", "claw", "jab", "swing", "lunge", "pierce",
                "cleave", "chop", "hack", "cut", "slay", "kill", "impale", "charge",
                "rush", "assault", "duel", "dispatch", "wound", "injure",
            ],
            "light_attack": [
                "poke", "prod", "tap", "flick", "nudge", "graze", "slap", "swat",
                "nip", "pinch", "scratch", "nick", "sting",
            ],
            "heavy_attack": [
                "smash", "crush", "slam", "bash", "wallop", "pulverize", "demolish",
                "obliterate", "annihilate", "devastate", "wreck", "destroy", "maul",
                "pummel", "batter", "clobber", "thrash", "bludgeon", "flay",
                "disembowel", "eviscerate", "shatter", "splinter", "stomp", "trample",
                "flatten", "sunder", "shred", "tear", "rend", "ravage", "mangle",
            ],
            "search": [
                "search", "scavenge", "track", "hunt", "forage", "rummage", "scout",
                "investigate", "probe", "survey", "scan", "sift", "dig", "delve",
                "uncover", "find", "locate", "seek", "patrol", "reconnoiter",
            ],
            "travel": [
                "travel", "go", "journey", "run", "walk", "move", "head", "sprint",
                "dash", "flee", "retreat", "advance", "march", "climb", "crawl",
                "swim", "fly", "leap", "jump", "enter", "exit", "leave", "return",
                "approach", "follow", "proceed", "venture", "roam", "wander", "trek",
                "traverse", "cross", "navigate", "descend", "ascend", "scale", "hike",
                "amble", "saunter", "stride", "stroll", "meander",
            ],
            "speak": [
                "speak", "talk", "converse", "tell", "articulate", "say", "ask",
                "whisper", "shout", "yell", "scream", "plead", "beg", "greet", "hail",
                "call", "demand", "command", "request", "question", "answer", "reply",
                "respond", "chat", "negotiate", "persuade", "taunt", "announce",
                "declare", "proclaim", "inform", "explain", "describe", "narrate",
                "recite", "address", "lecture", "debate", "argue", "discuss", "mock",
                "insult", "flatter", "praise", "apologize", "confess", "warn",
                "threaten", "order", "instruct", "advise", "suggest", "propose",
                "invite",
            ],
            "inspect": [
                "inspect", "look", "examine", "observe", "study", "check", "peer",
                "gaze", "glance", "read", "analyze", "appraise", "identify", "perceive",
                "watch", "view", "review", "assess", "evaluate", "sample", "taste",
                "smell", "sniff", "listen", "sense", "spot", "notice", "discern",
                "detect",
            ],
            "defend": [
                "block", "parry", "dodge", "evade", "deflect", "guard", "protect",
                "brace", "resist", "counter", "cover", "ward", "repel", "absorb",
                "withstand", "fortify", "barricade", "intercept", "fend",
            ],
            "use": [
                "use", "activate", "apply", "employ", "consume", "drink", "eat",
                "wield", "equip", "wear", "light", "ignite", "open", "close", "unlock",
                "lock", "pull", "push", "turn", "flip", "press", "trigger", "operate",
                "manipulate", "handle", "deploy", "utilize",
            ],
            "take": [
                "take", "grab", "pick", "collect", "gather", "loot", "steal", "snatch",
                "seize", "claim", "acquire", "pocket", "obtain", "procure", "get",
                "fetch", "retrieve", "receive", "capture", "catch", "nab", "pilfer",
                "plunder", "ransack", "pillage", "commandeer", "confiscate",
            ],
            "drop": [
                "drop", "discard", "release", "abandon", "place", "put", "set",
                "deposit", "store", "stash", "forsake", "forfeit", "yield",
                "surrender", "relinquish", "give", "deliver", "toss",
            ],
            "cast": [
                "cast", "conjure", "summon", "invoke", "enchant", "hex", "curse",
                "bless", "heal", "cure", "resurrect", "banish", "dispel", "channel",
                "charm", "bewitch", "incant", "chant", "recite", "intone",
            ],
            "sneak": [
                "sneak", "creep", "lurk", "hide", "stalk", "skulk", "tiptoe",
                "shadow", "vanish", "disappear", "cloak", "camouflage", "prowl",
                "sidle", "skulk",
            ],
            "rest": [
                "rest", "sleep", "camp", "meditate", "recover", "nap", "sit", "wait",
                "pause", "doze", "slumber", "repose", "lounge", "relax", "unwind",
                "halt", "stop", "stay", "remain", "hibernate", "linger", "tarry",
            ],
            "trade": [
                "trade", "buy", "sell", "barter", "exchange", "haggle", "offer",
                "purchase", "shop", "deal", "bargain", "swap", "peddle", "auction",
                "bid", "vend", "hawk", "market",
            ],
        }

    def _assemble_canon(self, action, subject, direction, instrument, modifiers, topic):
        result = {
            "action": action,
            "subject": subject,
            "direction": direction,
            "instrument": instrument,
            "modifiers": modifiers,
            "topic": topic
        }
        return result
    
    def _get_topic(self, tags):
        topic = ""
        for i in range(0, len(tags)):
            if tags[i][0] == "about":
                for j in range(i, len(tags)):
                    if tags[j][1] in ("NN", "NNS"):
                        topic = tags[j][0]
                        return topic
        return topic

    _degree_adverbs = {"very", "really", "extremely", "quite", "rather",
                       "incredibly", "terribly", "awfully", "exceptionally",
                       "remarkably", "so", "too", "most"}

    def _get_modifiers(self, tags, action=None):
        modifiers = []
        after_with = False
        for i, tag in enumerate(tags):
            if tag[0].lower() == "with" and tag[1] == "IN":
                after_with = True
            elif tag[1] == "RB":
                if tag[0].lower() in self._degree_adverbs:
                    continue
                modifiers.append(tag[0])
            elif after_with and tag[1] in ("NN", "NNS") and tag[0].lower() in self._manner_words:
                modifiers.append(tag[0])
        return modifiers

    _manner_words = {"haste", "caution", "care", "stealth", "fury", "rage",
                      "speed", "force", "grace", "precision", "vigor", "ease"}

    _number_words = {
        "zero": 0, "dozen": 12,
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    }

    def _parse_quantity(self, word):
        '''Parse a quantity word or number string into an integer, or return None'''
        low = word.lower()
        if low in self._number_words:
            return self._number_words[low]
        try:
            return int(word)
        except ValueError:
            return None

    def _get_instrument(self, tags, action=None):
        instruments = []
        for i in range(0, len(tags)):
            if tags[i][0] == "with":
                j = i + 1
                while j < len(tags):
                    quantity = 1
                    if tags[j][1] == "CD" or (tags[j][1] in ("NN", "NNS") and self._parse_quantity(tags[j][0]) is not None):
                        parsed = self._parse_quantity(tags[j][0])
                        if parsed is not None:
                            quantity = parsed
                        j += 1
                        if j >= len(tags):
                            break
                    if tags[j][1] in ("JJ", "NN", "NNS"):
                        if tags[j][1] in ("NN", "NNS") and tags[j][0].lower() in self._manner_words:
                            j += 1
                            continue
                        parts = [tags[j][0]]
                        found_noun = tags[j][1] in ("NN", "NNS")
                        while j+1 < len(tags) and tags[j+1][1] in ("JJ", "NN", "NNS"):
                            if tags[j+1][1] in ("NN", "NNS") and tags[j+1][0].lower() in self._manner_words:
                                break
                            if found_noun and tags[j+1][1] == "NNS":
                                break
                            parts.append(tags[j+1][0])
                            if tags[j+1][1] in ("NN", "NNS"):
                                found_noun = True
                            j += 1
                        if found_noun:
                            instruments.append({"name": " ".join(parts), "quantity": quantity})
                    j += 1
                return instruments
        return instruments

    def _get_direction(self, tags):
        direction = ""
        for tag in tags:
            if tag[1] == "DIR":
                direction = tag[0]
                return direction
        return direction
    
    def _get_canon(self, verb):
        verb = verb.lower()
        for canon, synonyms in self.canon.items():
            if verb in synonyms:
                return canon
        nlp = get_nlp()
        verb_doc = nlp(verb)
        best_score = -1
        best_canon = list(self.canon.keys())[0]
        for canon, synonyms in self.canon.items():
            for syn in synonyms:
                syn_doc = nlp(syn)
                score = verb_doc.similarity(syn_doc)
                if score > best_score:
                    best_score = score
                    best_canon = canon
        return best_canon

    def _get_verb_subject(self, tags: list[tuple]) -> str:
        '''get the noun phrase after the first verb'''
        verb = ""
        for i in range(len(tags)):
            if tags[i][1] in ("VB", "VBP", "VBD"):
                verb = tags[i][0]
                collecting = []
                has_noun = False
                last_subject = ""
                for j in range(i + 1, len(tags)):
                    tag = tags[j][1]
                    word = tags[j][0].lower()
                    if tag == "IN" and word in ("with", "about"):
                        '''words that end subject collection'''
                        break
                    elif tag in ("DT", "TO", "IN"):
                        if collecting and not has_noun:
                            collecting = []
                        elif collecting and has_noun:
                            last_subject = " ".join(collecting)
                            collecting = []
                            has_noun = False
                    elif tag in ("JJ", "DIR", "NN", "NNS"):
                        collecting.append(tags[j][0])
                        if tag in ("NN", "NNS"):
                            has_noun = True
                    elif collecting:
                        break
                if has_noun:
                    return verb, " ".join(collecting)
                if last_subject:
                    return verb, last_subject
                return verb, ""
        return verb, ""

    def _tokenize_directions(self, tags: list[tuple]) -> list[tuple]:
        '''tag any direction word with "DIR"'''
        new_tags = []
        direction_words = ["north", "east", "south", "west"]
        for i, tag in enumerate(tags):
            if tag[0] in direction_words:
                new_tag = (tag[0], "DIR")
                new_tags.append(new_tag)
            else:
                new_tags.append(tag)

        '''find compound directions'''
        tags = new_tags
        new_tags = []
        c = 0
        direction = ""
        while c < len(tags):
            if tags[c][1] == "DIR":
                if direction == "":
                    direction = tags[c][0]
                else:
                    direction = direction + " " + tags[c][0] 
            elif direction == "":
                new_tags.append(tags[c])
            else:
                new_tags.append((direction, "DIR"))
                new_tags.append(tags[c])
                direction = ""
            c += 1
        if direction != "":
            new_tags.append((direction, "DIR"))

        '''see if any directions are part of a noun'''
        tags = new_tags
        new_tags = []
        c = 0
        while c < len(tags):
            if c+1 < len(tags):
                if tags[c+1][1] == "NN" and tags[c][1] == "DIR":
                    new_tags.append((tags[c][0] + " " + tags[c+1][0], "NN"))
                    c += 1
                else:
                    new_tags.append(tags[c])
            else:
                new_tags.append(tags[c])
                break
            c += 1

        return new_tags

    def _has_verb(self, tokens: list[str]) -> bool:
        '''check if a token list contains a recognized canon verb'''
        canon_verbs = set()
        for verbs in self.canon.values():
            canon_verbs.update(verbs)
        return any(t.lower() in canon_verbs for t in tokens)

    def _get_compound_actions(self, tokens: list[str]) -> list[list[str]]:
        # Handle 'and', 'then', and 'or' as split points, but 'or' is random
        for keyword in ("and", "then"):
            if keyword in tokens:
                i = tokens.index(keyword)
                left = tokens[:i]
                right = tokens[i+1:]
                if not self._has_verb(right):
                    return [tokens[:i] + tokens[i+1:]]
                results = []
                if left:
                    results.extend(self._get_compound_actions(left))
                if right:
                    results.extend(self._get_compound_actions(right))
                return results
        if "or" in tokens:
            i = tokens.index("or")
            left = tokens[:i]
            right = tokens[i+1:]
            left_actions = self._get_compound_actions(left) if left else []
            right_actions = self._get_compound_actions(right) if right else []
            choice = random.choice(["left", "right", "both"])
            if choice == "left":
                return left_actions
            elif choice == "right":
                return right_actions
            else:
                return left_actions + right_actions
        elif "xor" in tokens:
            i = tokens.index("xor")
            left = tokens[:i]
            right = tokens[i+1:]
            left_actions = self._get_compound_actions(left) if left else []
            right_actions = self._get_compound_actions(right) if right else []
            choice = random.choice(["left", "right"])
            if choice == "left":
                return left_actions
            elif choice == "right":
                return right_actions
        elif "nand" in tokens:
            i = tokens.index("nand")
            left = tokens[:i]
            right = tokens[i+1:]
            left_actions = self._get_compound_actions(left) if left else []
            right_actions = self._get_compound_actions(right) if right else []
            choice = random.choice(["left", "right", "neither"])
            if choice == "left":
                return left_actions
            elif choice == "right":
                return right_actions
            else:
                return []
        elif "not" in tokens:
            i = tokens.index("not")
            right = tokens[i+1:]
            right_actions = self._get_compound_actions(right) if right else []
            choice = random.choice(["right"])
            if choice == "right":
                return []
            else:
                return left_actions + right_actions
        else:
            return [tokens]
        
    def _post_process(self, tags):
        new_tags = []
        canon_verbs = set()
        for verbs in self.canon.values():
            canon_verbs.update(verbs)
        found_verb = False
        for word, tag in tags:
            if not found_verb and word.lower() in canon_verbs:
                new_tags.append((word, "VBP"))
                found_verb = True
            elif found_verb and tag in ("VB", "VBP", "VBD") and word.lower() not in canon_verbs:
                new_tags.append((word, "NN"))
            else:
                new_tags.append((word, tag))
        return new_tags

    def _get_intent(self, action, debug: bool = False):
        tags: list[tuple] = pos_tag(action)
        tags = self._tokenize_directions(tags)
        tags = self._post_process(tags)
        verb, subject = self._get_verb_subject(tags)
        action = self._get_canon(verb)
        direction = self._get_direction(tags)
        instrument = self._get_instrument(tags, action)
        modifiers = self._get_modifiers(tags, action)
        topic = self._get_topic(tags)
        result = self._assemble_canon(action, subject, direction, instrument, modifiers, topic)
        if debug:
            print(action)
            print(tags)
            print(result)
            nlp = get_nlp()
            doc = nlp(" ".join(action))
            tags = [(token.text, token.tag_) for token in doc]
            tags = self._tokenize_directions(tags)
            tags = self._post_process(tags)
            verb, subject = self._get_verb_subject(tags)
            verb = self._get_canon(verb)
            direction = self._get_direction(tags)
        return result

    def run(self, user_input: str, debug = False) -> dict:
        tokens: list[str] = word_tokenize(user_input)
        actions = self._get_compound_actions(tokens=tokens)
        for action in actions:
            if action[0]:
                if action[0].lower() != "I":
                    action.insert(0, "I")
            result = self._get_intent(action=action, debug=debug)
        return result
        