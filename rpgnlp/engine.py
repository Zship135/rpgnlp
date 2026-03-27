
import os
import sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, brown
import string
from nltk.tag import pos_tag
import yaml
from rapidfuzz import fuzz, process
import json
import random

def _resource_path(relative_path: str) -> str:
    """Resolve path for bundled PyInstaller data files or normal dev."""
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)

class NLPEngine:
    def __init__(self):
        self.canon = self._load_canon()
        common_verbs = set([
            'open'
        ])
        self.adverbs = [word for word, pos in brown.tagged_words() if pos == 'RB' and word not in common_verbs]

    def _assemble_canon_event(self, action, subject, direction, modifiers, instrument=None):
        event = {}
        event["action"] = action
        event["subject"] = subject
        event["direction"] = direction
        event["modifiers"] = modifiers
        event["instrument"] = instrument
        return event

    def _parse_question(self, tags: list[tuple]) -> dict:
        question_words = ["who", "what", "when", "where", "why"]
        action, subject, direction, modifiers = None, None, None, None
        action = "question"
        for tag in tags:
            if tag[0] in question_words: modifiers = [tag[0]]
            if tag[0] == "i": subject = "i" 
        if modifiers is None: modifiers = self.get_modifiers(tags)
        if subject is None: subject = self.get_subject(tags) 
        direction = self.get_direction(tags=tags)
        return self.assemble_canon_event(action=action, subject=subject, direction=direction, modifiers=modifiers)


    def _get_canon_event(self, verb):
        canon_action = self.canon.get(verb)
        if canon_action is None:
            matches = process.extract(verb, self.canon.keys(), scorer=fuzz.WRatio, limit=2)
            if len(matches) > 0:
                if matches[0][1] >= 71:
                    canon_action = self.canon.get(matches[0][0])
        return canon_action

    def _load_canon(self):
        with open(_resource_path('vocab.yaml'), 'r') as file:
            canon = yaml.safe_load(file)
        inverted = {}
        for canon_action, data in canon.items():
            for verb in data["verbs"]:
                inverted[verb] = canon_action
        return inverted

    def _post_process_directions(self, tags: list) -> list:
        # Support multi-word directions
        direction_phrases = [
            ["north"], ["south"], ["east"], ["west"],
            ["north", "east"], ["north", "west"], ["south", "east"], ["south", "west"],
            ["n"], ["s"], ["e"], ["w"],
            ["n", "e"], ["n", "w"], ["s", "e"], ["s", "w"],
            ["forward"], ["backward"], ["left"], ["right"], ["back"], ["away"]
        ]
        direction_set = set([tuple(phrase) for phrase in direction_phrases])
        i = 0
        new_tags = []
        while i < len(tags):
            matched = False
            # Try to match 2-word directions first
            if i+1 < len(tags):
                two_word = (tags[i][0], tags[i+1][0])
                if two_word in direction_set:
                    new_tags.append((tags[i][0] + " " + tags[i+1][0], "DIR"))
                    i += 2
                    matched = True
            if not matched:
                # Try 1-word direction
                if (tags[i][0],) in direction_set:
                    new_tags.append((tags[i][0], "DIR"))
                else:
                    new_tags.append(tags[i])
                i += 1
        return new_tags
    
    def _post_process_adverbs(self, tags):
        new_tags = []
        for tag in tags:
            if tag[0] in self.adverbs:
                new_tags.append((tag[0], "RB"))
            else:
                new_tags.append(tag)
        return new_tags
                
    def _get_direction(self, tags):
        for i, tag in enumerate(tags):
            if tag[1] == "DIR":
                if i+1 < len(tags) and tags[i+1][1] == "NN":
                    continue
                return tag[0]
        return None

    def _get_subject(self, tags) -> str:
        subject = None
        for i, tag in enumerate(tags):
            '''Case 1 : JJ with NN with NN ...'''
            if tag[1] == "JJ":
                if i+1 < len(tags) and tags[i+1][1] == "NN":
                    subject = tag[0] + " " + tags[i+1][0]
                    return subject
            '''Case 2 : NN with NN with NN ...'''
            if tag[1] == "NN":
                if i+1 < len(tags) and tags[i+1][1] == "NN":
                    subject = tag[0] + " " + tags[i+1][0]
                else:
                    subject = tag[0]
                    return subject
                return subject 
            '''Case 3 : DIR with NN'''
            if tag[1] == "DIR":
                 if i+1 < len(tags) and tags[i+1][1] == "NN":
                    subject = tag[0] + " " + tags[i+1][0]
                    return subject
        return subject

    def _get_modifiers(self, tags):
        modifiers = []
        exceptions = ["over"]
        for tag in tags:
            if (tag[1] == "RB" or tag[1] == "IN") and tag[1] not in exceptions:
                modifiers.append(tag[0])
        return modifiers

    def _get_verb(self, tags):
        modal_verbs = ["want", "try", "attempt", "wish", "need", "hope", "plan", "decide"]
        verb = None
        for tag in tags:
            if tag[1] == "VBP" or tag[1] == "VB" or tag[1] == "VBD":
                if tag[0] in modal_verbs:
                    pass
                else:
                    verb = tag[0]
                    break
        return verb

    def _post_processing(self, tags: list) -> list:
        tags = self._post_process_adverbs(tags=tags)
        tags = self._post_process_directions(tags=tags)
        return tags

    def _parse_input(self, user_input, tags):
        if " and " in user_input:
            for i, tag in enumerate(tags):

                '''Case 1 : DIR + NN''' 
                if tag[1] == "DIR":
                    if i+1 < len(tags) and tags[i+1][1] == "NN":
                        return tag[0] + " " + tags[i+1][0]
                
                '''Case 2 : JJ + NN'''
                if tag[1] == "JJ":
                    if i+1 < len(tags) and tags[i+1][1] == "NN":
                        return tag[0] + " " + tags[i+1][0]
                
                '''Case 3 : NN + NN (e.g., 'south east gate')'''
                if tag[1] == "NN":
                    if i+1 < len(tags) and tags[i+1][1] == "NN":
                        return tag[0] + " " + tags[i+1][0]
                
                '''Case 4 : RB + JJ + NN'''
                if tag[1] == "RB":
                    if (i+1 < len(tags) and tags[i+1][1] == "JJ") and (i+2 < len(tags) and tags[i+2][1] == "NN"):
                        return tag[0] + " " + tags[i+1][0] + " " + tags[i+2][0]
            return None
        elif " or " in user_input:
            parts = user_input.split(" or ")
            return [random.choice(parts)]
        else:
            return [user_input]

    def _tokenize(self, user_input) -> list[str]:
        tokens: list[str] = word_tokenize(user_input.lower())
        if tokens[0] != "i":
            tokens.insert(0, "I")
        else:
            tokens.remove(tokens[0])
            tokens.insert(0, "I")
        return tokens

    def _get_intent(self, tags: list[tuple]):
        instrument = None
        tags_ = tags[:]
        if len(tags_) > 2 and tags_[0][0] == 'with':
            instr_tokens = []
            i = 1
            while i < len(tags_) and tags_[i][1] in ('DT', 'JJ', 'NN'):
                if tags_[i][1] != 'DT':
                    instr_tokens.append(tags_[i][0])
                i += 1
            if instr_tokens:
                instrument = ' '.join(instr_tokens)
            if i < len(tags_) and tags_[i][0] == ',':
                i += 1
            tags_ = tags_[i:]
        verb = self._get_verb(tags=tags_)
        subject = self._get_subject_after_verb(tags_)
        direction = self._get_direction(tags=tags_)
        modifiers = self._get_modifiers(tags=tags_)
        if tags and tags[0][0] == 'with' and 'with' not in modifiers:
            modifiers = ['with'] + (modifiers if modifiers else [])
        if not instrument:
            instrument = self._get_instrument(tags=tags_)
        action = self._get_canon_event(verb=verb)
        return action, subject, direction, modifiers, instrument

    def _get_subject_after_verb(self, tags):
        found_verb = False
        for i, tag in enumerate(tags):
            if not found_verb and tag[1].startswith('VB'):
                found_verb = True
                continue
            if found_verb:
                if tag[1] == 'JJ' and i+1 < len(tags) and tags[i+1][1] == 'NN':
                    return tag[0] + ' ' + tags[i+1][0]
                if tag[1] == 'NN':
                    return tag[0]
        return None

    def _get_instrument(self, tags):
        instrument = None
        for i, tag in enumerate(tags):
            if tag[0] == 'with':
                instr_tokens = []
                j = i + 1
                while j < len(tags) and tags[j][1] in ('DT', 'JJ', 'NN'):
                    if tags[j][1] != 'DT':
                        instr_tokens.append(tags[j][0])
                    j += 1
                if instr_tokens:
                    instrument = ' '.join(instr_tokens)
                    break
        return instrument

    def _tag(self, tokens: list[str]) -> list[tuple]:
        tags: list[tuple] = pos_tag(tokens)
        tags: list[tuple] = self._post_processing(tags=tags)
        tags.remove(tags[0])
        return tags

    def _is_question(self, tags: list[tuple]) -> bool:
        return tags[len(tags)-1][0] == "?"

    def run(self, user_input: str, debug = False) -> dict:
        event = None
        tokens: list[str] = self._tokenize(user_input=user_input)
        tags: list[tuple] = self._tag(tokens=tokens)
        if self._is_question(tags=tags):
            event = self._parse_question(tags=tags)
            return event
        action, subject, direction, modifiers, instrument = self._get_intent(tags=tags)
        if debug == True:
            print(tokens)
            print(tags)
            print(self._assemble_canon_event(action=action, subject=subject, direction=direction, modifiers=modifiers, instrument=instrument))
        return self._assemble_canon_event(action=action, subject=subject, direction=direction, modifiers=modifiers, instrument=instrument)

