
import os
import sys
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
import string
from nltk.tag import pos_tag
import yaml
from rapidfuzz import process
import json
import random
import spacy

_NLP = None

def get_nlp():
    global _NLP
    if _NLP is None:
        _NLP = spacy.load("en_core_web_md")
    return _NLP

class NLPEngine:
    def __init__(self):
        self.canon = {
            "attack": ["attack", "hit", "strike", "fight", "bonk", "whack", "punch", "slice", "slime"],
            "search": ["search", "scavenge", "track"],
            "heavy_attack": ["smash", "crush", "slam", "bash", "wallop", "pulverize", 
                            "demolish", "obliterate", "annihilate", "devastate", 
                            "wreck", "ruin", "destroy", "maul", "pummel", "batter", 
                            "clobber", "thrash", "beat", "bludgeon", "club", "flay", 
                            "skin", "disembowel", "eviscerate", "demolish"],
            "travel": ["travel", "go", "journey", "run"],
            "speak": ["speak", "talk", "utter", "converse", "tell", "articulate"],
            "inspect": ["inspect", "look"]
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

    def _get_modifiers(self, tags, action=None):
        modifiers = []
        after_with = False
        for tag in tags:
            if tag[0].lower() == "with" and tag[1] == "IN":
                after_with = True
            elif tag[1] == "RB":
                modifiers.append(tag[0])
            elif after_with and tag[1] in ("NN", "NNS") and tag[0].lower() in self._manner_words:
                modifiers.append(tag[0])
        return modifiers

    _manner_words = {"haste", "caution", "care", "stealth", "fury", "rage",
                      "speed", "force", "grace", "precision", "vigor", "ease"}

    def _get_instrument(self, tags, action=None):
        instruments = []
        for i in range(0, len(tags)):
            if tags[i][0] == "with":
                j = i + 1
                while j < len(tags):
                    if tags[j][1] in ("JJ", "NN"):
                        if tags[j][1] == "NN" and tags[j][0].lower() in self._manner_words:
                            j += 1
                            continue
                        # Collect adjectives and nouns as a compound instrument
                        parts = [tags[j][0]]
                        found_noun = tags[j][1] == "NN"
                        while j+1 < len(tags) and tags[j+1][1] in ("JJ", "NN"):
                            if tags[j+1][1] == "NN" and tags[j+1][0].lower() in self._manner_words:
                                break
                            parts.append(tags[j+1][0])
                            if tags[j+1][1] == "NN":
                                found_noun = True
                            j += 1
                        if found_noun:
                            instruments.append(" ".join(parts))
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
        # Exact match
        for canon, synonyms in self.canon.items():
            if verb in synonyms:
                return canon
        # Always use semantic similarity for best guess
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
        # Handle 'and' and 'or' as split points, but 'or' is random
        if "and" in tokens:
            i = tokens.index("and")
            left = tokens[:i]
            right = tokens[i+1:]
            # Only split if the right side contains a verb (i.e. it's a separate action)
            if not self._has_verb(right):
                return [tokens[:i] + tokens[i+1:]]
            results = []
            if left:
                results.extend(self._get_compound_actions(left))
            if right:
                results.extend(self._get_compound_actions(right))
            return results
        elif "or" in tokens:
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
        