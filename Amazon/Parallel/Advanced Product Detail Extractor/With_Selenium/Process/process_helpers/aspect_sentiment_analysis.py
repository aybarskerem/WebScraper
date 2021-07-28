import stanza
from .unicode_safe_print import unicode_safe_print
from .polarity_sentiment_analysis import get_overall_sentimentPolarity

stanzaPipeline = stanza.Pipeline('en')
def aspectBased_sentiment_analysis(inputString):

  '''
  Description of the algorithm:
    - Consider the sentences:
      1) This computer is bad
      2) This is a bad computer
      3) This can turn a bad computer into a good one

    In the 1st sentence PC is specified as "nsubj" of "bad"  by the stanza algorithm where as for the 2nd and 3rd, bad/good is specified as "amod" of PC. So; we will check the case from the point of adjectives and then from the perspective of nouns; then check for 'nsubj'

    Adverb handling:
    ================
    - very good, so much good, so good and good will reduce to "good" only
    - not very good", "not su much good", "not so good", "not good", "not good at all" etc. will all reduce to "not good" only.
    
    - To achieve this, we will first process the dependency array while distinguishing each separate adjective even if they are the same adjectives (separation will be with the help of the ids); then each adjective will be reduced to simple form like "good" and "not good" without any adverbs etc.; then we will merge the same adjectives i.e. the lists represented by the adjectives which are reduced to "good" will be merged among themselves. The same applies for adjectives like "not good".
  '''
  #unicode_safe_print('###################################')
  #unicode_safe_print(inputString)

  doc = stanzaPipeline(inputString) # https://stanfordnlp.github.io/stanza/data_objects.html
  doc.text = doc.text.lower()
  
  resulting_noun_adjectiveList_dict = {}
  for sentence in doc.sentences:
    # unicode_safe_print('*********************')
    # unicode_safe_print(sentence.text)
    # unicode_safe_print(sentence.dependencies)

    dep_dict = {} # dependency dictionary
    initialize_dep_dict(dep_dict, sentence)

    # unicode_safe_print('initialize_dep_dict*********************')
    # unicode_safe_print(dep_dict)
    
    adjElem_nounElemList_dict = get_adjElem_nounElemList_dict(dep_dict, sentence)

    # unicode_safe_print('adjElem_nounElemList_dict*********************')
    # unicode_safe_print(adjElem_nounElemList_dict)

    for adjElem in adjElem_nounElemList_dict:
      dep_dict[adjElem]['nouns'] = list(adjElem_nounElemList_dict[adjElem])
    
    # unicode_safe_print('nounGroup assigning*********************')
    # unicode_safe_print(dep_dict)

    convert_each_adjElem_to_plainAdjLists(dep_dict)

    # unicode_safe_print('convert_each_adjElem_to_plainAdjLists*********************')
    # unicode_safe_print(dep_dict)

    flatten_Nouns_and_Adjectives(dep_dict)

    # unicode_safe_print('flatten_Nouns_and_Adjectives*********************')
    # unicode_safe_print(dep_dict)
    
    adjective_nounList_dict = get_adjective_nounList_dict(dep_dict)
    del dep_dict # it is not used anymore

    # unicode_safe_print('adjective_nounList_dict*********************')
    # unicode_safe_print(adjective_nounList_dict)

    noun_adjectiveList_dict = convert_to_nounAdjectiveList(adjective_nounList_dict)
    del adjective_nounList_dict # it is not used anymore

    # unicode_safe_print('noun_adjectiveList_dict*********************')
    # unicode_safe_print(noun_adjectiveList_dict)

    for noun, adjList in noun_adjectiveList_dict.items(): # update the retVal dictionary with the result of this sentence
      resulting_noun_adjectiveList_dict.setdefault(noun, []).extend(adjList)
  
  # unicode_safe_print('*********************')
  # unicode_safe_print(resulting_noun_adjectiveList_dict)

  retVal = filterOutNonSignificantAdjectives(resulting_noun_adjectiveList_dict)
  # unicode_safe_print('********************* FINAL RESULT *********************')
  # unicode_safe_print(retVal)
  return retVal

def get_adjective_nounList_dict(dep_dict):
  '''
  Processes to discard adjectives which do not include 'nouns' key. Also,  negate adjectives if they contain 'negation' keyword and remove the ids in the adjectives hence merging the same ones ('BIG',12 ) and ('BIG', 25) would be merged to 'BIG' if they both are non-negated where 12 and 25 are their ids respectively.

  Each element in resulting nounList is unique.
  Converts
  {('BIG', 4): {'nouns': ['HOUSE']}, ('LARGE', 6): {'nouns': ['HOUSE']}, ('GOOD', 12): {'nouns': ['NOT CAR']}} 
  to
  {'BIG': {'HOUSE'}, 'LARGE': {'HOUSE'}, 'GOOD': {'NOT CAR'}}

  OR 
  {('BIG', 10): {'nouns': ['PC'], 'adjectives': ['NOT TINY', 'NOT SMALL']}, ('SMALL', 13): {'negation': 'NOT', 'adjectives': ['NOT TINY']}, ('TINY', 15): {'and_or': {'OR'}}} 
  to
  {'NOT TINY': {'PC'}, 'NOT SMALL': {'PC'}, 'BIG': {'PC'}}

  OR
  {'IS_SENTENCE_NEGATED': {'YES'}, ('GOOD', 5): {'nouns': ['SPEED']}, ('LONG', 11): {'nouns': ['CABLE'], 'negation': 'NOT'}}
  to
  {'NOT GOOD': {'SPEED'}, 'LONG': {'CABLE'}}

  '''

  IS_SENTENCE_NEGATED = 'IS_SENTENCE_NEGATED' in dep_dict
  adjective_nounList_dict = {}
  for adjElem, value in dep_dict.items():
    if not 'nouns' in value:
      continue
    if 'adjectives' in value:
      for adj in value['adjectives']:
        if IS_SENTENCE_NEGATED:
          if adj.startswith('NOT '):
            adjective_nounList_dict.setdefault(adj[4:], set()).update(value['nouns']) # non-negate (remove the 'NOT ') from the adjective
          else:
            adjective_nounList_dict.setdefault('NOT ' + adj, set()).update(value['nouns'])          
        else:
          adjective_nounList_dict.setdefault(adj, set()).update(value['nouns'])

    if 'negation' in value:
      if IS_SENTENCE_NEGATED:
        adjective_nounList_dict.setdefault(adjElem[0], set()).update(value['nouns'])
      else:
        adjective_nounList_dict.setdefault('NOT ' + adjElem[0], set()).update(value['nouns'])

    else:
      if IS_SENTENCE_NEGATED:
        adjective_nounList_dict.setdefault('NOT ' + adjElem[0], set()).update(value['nouns'])
      else:
        adjective_nounList_dict.setdefault(adjElem[0], set()).update(value['nouns'])
  
  return adjective_nounList_dict

def filterOutNonSignificantAdjectives(resulting_noun_adjectiveList_dict):
  '''
  Filter out adjectives not contributing any negativity or positivity to the nouns.
  e.g. Convert
  {'HOUSE': ['BIG', 'LARGE'], 'CAR': ['NOT GOOD']}
  to
  {'CAR': ['NOT GOOD']}
  since big and large do not add any negativity or positivity to the car.
  '''
  retVal = {}
  for noun, adjList in resulting_noun_adjectiveList_dict.items():
    for adj in adjList:
      noun_with_qualifying_adjective = adj + " " + noun # e.g. { QUALITY: [GREAT] } -> GREAT QUALITY
      adj_sentiment = get_overall_sentimentPolarity(noun_with_qualifying_adjective)
      if adj_sentiment != 'neutral': # only add if it has importance (i.e. adding positivity or negativity qualification to the name )
        retVal.setdefault(noun, set()).add(adj)
  
  for noun, adjSet in retVal.items(): # convert sets to lists
    retVal[noun] = list(adjSet)

  return retVal


def convert_to_nameElem_adjList(adjective_nounList_dict):
  '''
    Converts adjective&name key&value pairs to name&adjective key&value pairs
    e.g. Converts 
    {('BIG', 4): {'nouns': [('CAR', 10)], 'adjectives': [('GOOD', 9)]}, ('LARGE', 6): {'nouns': [('CAR', 10)]}, ('GOOD', 9): {'negation': 'NOT'}, ('BAD', 14): {'nouns': [('DOG', 15)]}}
    to
    {('CAR', 10): [('BIG', 4), ('LARGE', 6)], ('DOG', 15): [('BAD', 14)]}
  '''
  new_dict = {}
  for key, value in adjective_nounList_dict.items():
    if 'nouns' in value:
      for name in value['nouns']:
        new_dict.setdefault(name, []).append(key)
  
  return new_dict

def convert_to_nounAdjectiveList(adjective_nounList_dict):
  '''
    Converts each adjective&name key&value pairs inside the input dict to name&adjective key&value pairs
    e.g. 
    Converts 
    {'GOOD': {('SPEED', 4)}, 'NICE': {('SCREEN', 9)}, 'PERFECT': {('SCREEN', 9)}} to
    {'SPEED': ['GOOD'], 'SCREEN': ['NICE', 'PERFECT']}
    OR
    {'GOOD': {('IDEA', 6, 'NOT')}} to 
    {'IDEA': ['NOT GOOD']}
  '''
  new_dict = {}
  for adj, nounList in adjective_nounList_dict.items():
    for noun in nounList:
      new_dict.setdefault(noun, []).append(adj)
  
  return new_dict

def _findRelatedNouns(sentence):
  '''
  Example sentence: "It has good speed, a nice perfect screen and keyboard."
   GROUP RELATED NAMES TOGETHER e.g. {('SPEED', 4): [('SPEED', 4), ('SCREEN', 9), ('KEYBOARD', 11)], ('SCREEN', 9): [('SCREEN', 9)], ('KEYBOARD', 11): [('KEYBOARD', 11)]}
  '''
  nameGroups={}
  for token in sentence.tokens:  
    if (token.words[0].upos == 'NOUN' or token.words[0].upos == 'PROPN'):
      tokenProps = token.words[0]
      nameGroups.setdefault((tokenProps.lemma.upper(), tokenProps.id), []).append( 
        (tokenProps.lemma.upper(), tokenProps.id) ) # add the name itself to the group of related names list before adding the related names

      if tokenProps.deprel == 'conj': # handle names having related names to itself (if any related name exists)
        relatedParentNameProps = sentence.tokens[tokenProps.head-1].words[0]
        nameGroups.setdefault( (relatedParentNameProps.lemma.upper(), relatedParentNameProps.id), [] ).append((tokenProps.lemma.upper(), tokenProps.id) )
  return nameGroups

def _mapCorrectAdjectivesToNounGroups(dep_dict, nounGroups):
  '''
  Returns a dict where keys are nounElems (noun/id pairs) and the values are adjElem (adjective/id pair) lists.

  # "It has good speed, a nice perfect screen and keyboard."
  # We groped nameds e.g. {('SPEED', 4): [('SPEED', 4), ('SCREEN', 9), ('KEYBOARD', 11)], ('SCREEN', 9): [('SCREEN', 9)], ('KEYBOARD', 11): [('KEYBOARD', 11)]}
  # But, it would be wrong if we assign ('SPEED', 4) adjectives to all elem inside  [('SPEED', 4), ('SCREEN', 9), ('KEYBOARD', 11)] for example since these names being related does not mean they share the same adjective.
  
  # "It has good speed, a nice perfect screen and keyboard." In this sentence speed, screen and keyboard are related but screen and keyboard have different adjective qualifying themselves. If we assign speed's adjective(s) to them; they would all have 'good' as an adjective as well as their own adjectives like 'nice' and 'perfec' for screen. However, speed is qualified by good only and screen/keyboard are qualified by the same adjective 'nice'. But, how can we know keyboard is qualified by 'nice' but not 'good'? Since we know that 'nice' comes after 'good' and already qualifies another noun; then it means the names coming after 'nice' can only be qualified by 'nice' or adjectives coming after 'nice' if any. So, for list [('SPEED', 4), ('SCREEN', 9), ('KEYBOARD', 11)], we check the adjectives of ('SPEED', 4) in dep_dict and we find 'good' and assign it to ('SPEED', 4) key. Then, for ('SCREEN', 9) we check if ('SCREEN', 9) has any adjectives qualifying it and we find 'nice' and 'perfect' so we assign these to ('SCREEN', 9) key. Then, for ('KEYBOARD', 11), we see that no adjectives qualfying it; so check the nearest preceding adjective which is of ('SCREEN', 9)'s and the adjectives are 'nice' and 'perfect so we assign these adjectives to ('KEYBOARD', 11). 

  # In the end, we get: {('SPEED', 4): {('GOOD', 3)}, ('SCREEN', 9): {('NICE', 7), ('PERFECT', 8)}, ('KEYBOARD', 11): {('NICE', 7), ('PERFECT', 8)}}
  '''
  nameElem_adjList_dict = convert_to_nameElem_adjList(dep_dict) # extra
  retVal = {}
  for _, nameElemList in nounGroups.items():
    lastValidInd = -1
    for i, nameElem in enumerate(nameElemList):
      if nameElem in nameElem_adjList_dict: # this name already has adjectives qualifying it.
        lastValidInd = i
      if lastValidInd != -1:
        retVal.setdefault(nameElem, set()).update(nameElem_adjList_dict[ nameElemList[lastValidInd] ])
  
  return retVal
def get_adjElem_nounElemList_dict(dep_dict, sentence):
  # Consider the sentence "It has good speed, a nice perfect screen and keyboard." for the explanations of each block in this function
  
  # we get {('SPEED', 4): [('SPEED', 4), ('SCREEN', 9), ('KEYBOARD', 11)], ('SCREEN', 9): [('SCREEN', 9)], ('KEYBOARD', 11): [('KEYBOARD', 11)]}
  nounGroups=_findRelatedNouns(sentence) # GROUP RELATED NAMES TOGETHER

  # unicode_safe_print("noun groups")
  # unicode_safe_print(nounGroups)

  # we get: {('SPEED', 4): {('GOOD', 3)}, ('SCREEN', 9): {('NICE', 7), ('PERFECT', 8)}, ('KEYBOARD', 11): {('NICE', 7), ('PERFECT', 8)}}
  retVal_nounElem_adjElemList_form = _mapCorrectAdjectivesToNounGroups(dep_dict, nounGroups )

  # unicode_safe_print("_mapCorrectAdjectivesToNounGroups")
  # unicode_safe_print(retVal_nounElem_adjElemList_form)

  # Switch keys and values
  retVal_adjElem_nounElemList_form = {}
  for nounElem, adjElemList in retVal_nounElem_adjElemList_form.items():
    for adjElem in adjElemList:
      retVal_adjElem_nounElemList_form.setdefault(adjElem, set()).add(nounElem[0])

  # FINAL RESULT: {('GOOD', 3): {'SPEED'}, ('PERFECT', 8): {'SCREEN', 'KEYBOARD'}, ('NICE', 7): {'SCREEN', 'KEYBOARD'}} 
  return retVal_adjElem_nounElemList_form


def flatten_Nouns_and_Adjectives(dep_dict):
  '''
  Flattens list of lists for values pointed by 'nouns' & 'adjectives' to lists and removes duplicates

  e.g. Converts {('BIG', 12): {'nouns': [('PC', 2)], 'negation': 'NOT', 'adjectives': [['NOT TINY', 'NOT SMALL']]}, ('SMALL', 15): {'negation': 'NOT', 'adjectives': [['NOT TINY']]}, ('TINY', 17): {'and_or': {'OR'}}}
  to
  {('BIG', 12): {'nouns': ['PC'], 'negation': 'NOT', 'adjectives': ['NOT SMALL', 'NOT TINY']}, ('SMALL', 15): {'negation': 'NOT', 'adjectives': ['NOT TINY']}, ('TINY', 17): {'and_or': {'OR'}}}

  OR

  {('BIG', 4): {'nouns': [('HOUSE', 7)]}, ('LARGE', 6): {'nouns': [('HOUSE', 7)]}, ('GOOD', 12): {'nouns': [('CAR', 13, 'NOT')]}}
  to
  {('BIG', 4): {'nouns': ['HOUSE']}, ('LARGE', 6): {'nouns': ['HOUSE']}, ('GOOD', 12): {'nouns': ['NOT CAR']}}

  '''
  for _, value in dep_dict.items():
    # flattenedNounSet = set()
    # if 'nouns' in value:
    #   flattenedNounSet.update(value['nouns'])
    # value['nouns'] = list(flattenedNounSet)

    if 'adjectives' in value:
      flattenedAdjSet = set()
      for adjList in value['adjectives']:
        flattenedAdjSet.update(adjList) 
      value['adjectives'] = list(flattenedAdjSet)


def convert_each_adjElem_to_plainAdjLists(dep_dict):
  '''
  Converts each adjElem (adjective/id pair) pointed by 'adjectives' keys (if any) into a list of adjective(s), by recursively inspecting each adjective in case they have other related adjectives to themselves (i.e. 'adjectives' key exists for the corresponding adjElem (adjective/id pair) ).

  Since in the list pointed by 'adjectives' key, there are multiple adjectives and since we return a list for each adjective there; after calling this function 'adjectives' key point to a list of list of adjectives.

  We should also be able to negate the child according to parent: not big or good is the same as not big or not good; so we should pass parent's negation information to the child

  e.g. 'adjectives':[(BAD, 12), (GOOD, 25)] can be converted to  'adjectives':[ [] , [NOT GOOD, BIG, TINY] ]; if (BAD, 12) keyed value has 'nouns' attribute (hence actually qualifying other nouns ) and (GOOD, 25) has 'negation' attribute and related adjectives big & tiny (where related adjectives determined recursively meaning we check for example ('BIG',25) and ('TINY', 12) keyed values possibly ('TINY', 12) being hidden in the 'adjectives' of ('BIG', 25)) 

  NOTE: This function does not convert dep_dict keys (which are also adjElems) to adjective lists. 
  '''
  for key in dep_dict:
    isNegated = 'negation' in dep_dict[key]
    if 'adjectives' in dep_dict[key]:
      for index, adj_elem in enumerate(dep_dict[key]['adjectives']):
        retVal = []
        if _setAdjectiveGroups_Recursive(dep_dict, adj_elem, isNegated, retVal):
          dep_dict[key]['adjectives'][index] = retVal[:]
        
def _setAdjectiveGroups_Recursive(dep_dict, key, isParentNegated, retVal):
  
  if type(key) is tuple: #if not tuple, then it is already processed
    if key in dep_dict: # keys cannot be lists etc (must be immutable); the key is a list only if the adjective which the key represents is already processed. 
      if 'nouns' in dep_dict[key]: # if the related adjective has nouns property; then it means the dependent adjective actually qualifies other noun(s), so we should not add add this adjective to our adjective list at all; so do not add anything to retVal (since we pass an empty list for retVal; it means discarding the adjective altogether) (e.g. [(BAD, 12), (GOOD, 25)] -> [ [] , [NOT GOOD] ] etc.
        return True
      
      isNegated = 'negation' in dep_dict[key] or isParentNegated # if itself or its parent is negated; then negate
      if 'adjectives' in dep_dict[key]: # it might only have 'negation' as the key without any related adjectives
        for index, adj_elem in enumerate(dep_dict[key]['adjectives']):      
          if _setAdjectiveGroups_Recursive(dep_dict, adj_elem, isNegated, retVal):  # No need to set dep_dict[key]['adjectives'][index] (change adj_elem in other words) if it is already processed; otherwise we would have set it to an empty list after processing which is wrong. Use depth-first approach; since retVal should grow bigger starting form the child helping us to convert all adjective-id groups to full adjective forms (negation and related adjectives included form) 
            dep_dict[key]['adjectives'][index] = retVal[:] # set the child value to kind of memoize the result  

      #if isNegated or ('and_or' in dep_dict[key] and isParentNegated): # the 2nd part of this if statement makes (not small and/or tiny) NOT SMALL, NOT TINY since the not should also apply to what comes after 'or'
      if isNegated: 
        retVal.append('NOT ' + key[0]) 
      else:
        retVal.append(key[0]) 
    else:
      retVal.append(key[0])
  else:
    return False

  return True
def handle_dependeeAdjective_initialization(dep_dict, word, dependentWord):
  '''
  dependee (parent) adjective = adjective which others depends on (in our case some nouns, adjectives, 'not' and 'and/or' depends on a parent adjective)
  '''
  if word.upos == 'ADJ':
      if dependentWord.upos == 'NOUN' or dependentWord.upos == 'PROPN' or dependentWord.upos == 'ADJ' or dependentWord.lemma.upper() == 'NOT' or dependentWord.lemma.upper() == 'AND' or dependentWord.lemma.upper() == '&' or dependentWord.lemma.upper() == 'OR' or dependentWord.lemma.upper() == '|': # if noun (whether it be a common noun or a proper noun); no need to add an ID

        
        if word.text.upper() != dependentWord.text.upper(): # for sentences like "This PC is not very big but so much good; but beds are not that big either"; due to either referring to the first usage of the big; the two bigs are related with a dependency relation of 'conj', but we do not want to consider those. Note that for unlogical sentences like "This PC is not very big but so much good; but beds are not that long either"; since stanza could not find any 'long' adjective before 'either', it does not even count 'long' as adjective but adverb somehow (in this sentence long is not found to be related to the 1st 'big' adjective since either probably expects a similar/same adjective )
          adjElem_key    = (word.lemma.upper(), word.id)
          nounElem_value = (dependentWord.lemma.upper(), dependentWord.id)

          if dependentWord.upos == 'ADJ' and dependentWord.deprel == 'conj':
            dep_dict.setdefault(adjElem_key, dict()).setdefault('adjectives', []).append( nounElem_value )
          elif (dependentWord.upos == 'NOUN' or dependentWord.upos == 'PROPN') and dependentWord.deprel == 'nsubj':
            # we do not need to distinguish the names and not from each other since they are already in the same adjective dependency list; however we need the ids for adjectives because we have to check if they have a dependency word "not" to know if it is a negated adjective or not (which we can only know by processing the dict again) 
            
            dep_dict.setdefault(adjElem_key, dict()).setdefault('nouns', []).append( nounElem_value )
            if ('NEGATED_NOUNS' in dep_dict) and (nounElem_value in dep_dict['NEGATED_NOUNS']): # In sentence 'not a very good idea', idea is a negated noun since in stanza, 'not' in this sentence qualifies the idea instead of 'good'; so we will make 'not' refer to 'good' by ourselves.
              if 'negation' in dep_dict[adjElem_key]:
                del dep_dict[adjElem_key]['negation'] # negations cancelled out each other
              else:
                dep_dict.setdefault(adjElem_key, dict())['negation'] = 'NOT'

          elif dependentWord.lemma.upper() == 'NOT': # 'negation' key only used to check if it exists at all, its value (which is 'not') is not important but just kept here to be able to make it conform to a dict architecture 
            dep_dict.setdefault(adjElem_key, dict())['negation'] = 'NOT'
          elif dependentWord.lemma.upper() == 'AND' or dependentWord.lemma.upper() == '&' or dependentWord.lemma.upper() == 'OR' or dependentWord.lemma.upper() == '|': # 'and_or' key only used to check if it exists at all, its value (which can be a set of 'and, or, &, |' ) is not important but just kept here to be able to make it conform to a dict architecture 
            dep_dict.setdefault(adjElem_key, dict()).setdefault('and_or', set()).add(dependentWord.lemma.upper())

def handle_negated_sentence(dep_dict, word, dependentWord):
  '''
  If the sentence include 'have not' in any form in a sentence (doesn't have, don't have, do not have, does not have, not have etc., all the adjectives in this sentence should be negated).

  Adds a 'IS_SENTENCE_NEGATED' key to indicate 'Negate all adjectives in this sentence since it includes "not have" negation in it.'

  NOTE: Consider the sentence, "My time and space in Italy were not very enjoyable and not fun."  # when be verbs are used it is hard to know if it is meant were 'very enjoyable and not fun' or meant were not 'very enjoyable and not fun'. We asssume it is the first one; so we do not double negate for these kinds of sentences even though we double negate for 'have not' verbs.
  '''
  if word.upos == 'VERB' and word.lemma.upper() == 'HAVE' and dependentWord.lemma.upper() == 'NOT' and dependentWord.deprel == 'advmod':
    dep_dict['IS_SENTENCE_NEGATED'] = set(['YES'])

def handle_dependeeNoun_initialization_forAdjectiveDependency(dep_dict, word, dependentWord):
  '''
  Prequisites: handle_dependeeNoun_initialization_forNegatedNounDependency function should have been called on dep_dict before
  dependee (parent) noun = noun which others depend on (in our case some adjectives depends on a parent noun)
  '''

  if word.upos == 'NOUN' or word.upos == 'PROPN': # we do not care if it is a noun (common noun) or a proper noun (nouns for specific things) as long as it is a noun
    if dependentWord.upos == 'ADJ' and (dependentWord.deprel == 'amod' or dependentWord.deprel == 'conj'): # if noun (whether it be a common noun or a proper noun); no need to add an ID
      adjElem_key    = (dependentWord.lemma.upper(), dependentWord.id)
      nounElem_value = (word.lemma.upper(), word.id)

      dep_dict.setdefault((dependentWord.lemma.upper(), dependentWord.id), dict()).setdefault('nouns', []).append( nounElem_value )
      if ('NEGATED_NOUNS' in dep_dict) and (nounElem_value in dep_dict['NEGATED_NOUNS']):
        if 'negation' in dep_dict[adjElem_key]:
          del dep_dict[adjElem_key]['negation'] # negations cancelled out each other
        else:
          dep_dict.setdefault(adjElem_key, dict())['negation'] = 'NOT'

def handle_dependeeNoun_initialization_forNegatedNounDependency(dep_dict, word, dependentWord):
  '''
  dependee noun = noun which others depend on (in our case some 'not's depends on a parent noun)
  '''
  if word.upos == 'NOUN' or word.upos == 'PROPN': # we do not care if it is a noun (common noun) or a proper noun (nouns for specific things) as long as it is a noun
    if dependentWord.lemma.upper() == 'NOT' and dependentWord.deprel == 'advmod':
      dep_dict.setdefault('NEGATED_NOUNS', set()).add( (word.lemma.upper(), word.id) )

def initialize_dep_dict(dep_dict, sentence):
  for word, dependencyRelation, dependentWord in sentence.dependencies:
    handle_negated_sentence(dep_dict, word, dependentWord)
    handle_dependeeNoun_initialization_forNegatedNounDependency(dep_dict, word, dependentWord)
    handle_dependeeAdjective_initialization(dep_dict, word, dependentWord) 
    handle_dependeeNoun_initialization_forAdjectiveDependency(dep_dict, word, dependentWord)
  
  if 'NEGATED_NOUNS' in dep_dict:
    del dep_dict['NEGATED_NOUNS']


########################### EXAMPLE INPUT STRINGS for aspectBased_sentiment_analysis FUNCTION ###########################

# txt = "My time and space in Italy were not very enjoyable and not fun."  # when be verbs are used it is hard to know if it is meant were 'very enjoyable and not fun' or meant were not 'very enjoyable and not fun'. We asssume it is the first one; so we do not double negate for these kinds of sentences even though we double negate for 'have not' verbs.

# Before removing non-significant adjectives: {'TIME': ['NOT FUN', 'NOT ENJOYABLE'], 'SPACE': ['NOT FUN', 'NOT ENJOYABLE']}
# After removing non-significant adjectives:  {'TIME': ['NOT FUN', 'NOT ENJOYABLE'], 'SPACE': ['NOT FUN', 'NOT ENJOYABLE']} since all the adjectives here add negativity or positivity to the nouns that they qualify

# txt = "My time and space in Italy were not very enjoyable and fun." 
# {'SPACE': ['NOT FUN', 'NOT ENJOYABLE'], 'TIME': ['NOT FUN', 'NOT ENJOYABLE']}
# {'SPACE': ['NOT FUN', 'NOT ENJOYABLE'], 'TIME': ['NOT FUN', 'NOT ENJOYABLE']}

# txt = "This PC, my room and the universe are not very big but not small or tiny either; also beds are not that big."
# txt = "This PC, my room and the universe are not very big but not small or tiny either"
# All adjectives:   {'ROOM': ['NOT TINY', 'NOT SMALL', 'NOT BIG'], 'UNIVERSE': ['NOT TINY', 'NOT SMALL', 'NOT BIG'], 'PC': ['NOT TINY', 'NOT SMALL', 'NOT BIG']}
# Significant ones: {}

# txt = "This PC, my room and the universe are big, not small and tiny"
# All adjectives:   {'UNIVERSE': ['NOT TINY', 'NOT SMALL', 'BIG'], 'PC': ['NOT TINY', 'NOT SMALL', 'BIG'], 'ROOM': ['NOT TINY', 'NOT SMALL', 'BIG']}
# Significant ones: {}

# txt = "These are good PC, not nice room or universe."
# Before removing non-significant adjectives: {'ROOM': ['NOT TINY', 'NOT SMALL', 'BIG'], 'UNIVERSE': ['NOT TINY', 'NOT SMALL', 'BIG'], 'PC': ['NOT TINY', 'NOT SMALL', 'BIG']}
# After removing non-significant adjectives: {} since none of the adjectives here add negativity or positivity to the nouns that they qualify

# txt = "this laptop has been great....good speed, nice screen, keyboard...hard to go wrong if one needs a back up laptop, one for a student- child....a lot of oomph at a fabulous price"
# {'LAPTOP': ['GREAT'], 'SPEED': ['GOOD'], 'SCREEN': ['NICE'], 'KEYBOARD': ['NICE'], 'PRICE': ['FABULOUS']}

#txt = "this laptop has been great. It has good speed, a nice screen and keyboard."
# {'LAPTOP': ['GREAT'], 'SPEED': ['GOOD'], 'SCREEN': ['NICE'], 'KEYBOARD': ['NICE']}

# txt = "It has good speed, a nice perfect screen and keyboard."
# {'SPEED': ['GOOD'], 'SCREEN': ['NICE', 'PERFECT'], 'KEYBOARD': ['NICE', 'PERFECT']}

# txt = "I have a big, large house and not a very good car."
# All adjectives:   {'HOUSE': ['BIG', 'LARGE'], 'CAR': ['NOT GOOD']}
# Significant ones: {'CAR': ['NOT GOOD']

# txt = "It has good speed and not a very long cable"
# All adjectives:   {'SPEED': ['GOOD'], 'CABLE': ['NOT LONG']}
# Significant ones: {'SPEED': ['GOOD']}

# txt = "It does not have good speed and not a very long cable"
# All adjectives:   {'SPEED': ['NOT GOOD'], 'CABLE': ['LONG']}
# Significant ones: {'SPEED': ['NOT GOOD']}

# txt = "It doesn't have good speed and a very long cable"
# All adjectives:   {'SPEED': ['NOT GOOD'], 'CABLE': ['NOT LONG']}
# Significant ones: {'SPEED': ['NOT GOOD']

# txt = "It has good speed and not very long cable" 
# {'SPEED': ['GOOD'], 'CABLE': ['NOT LONG']}
# {'SPEED': ['GOOD']}

#txt = "this laptop has been great....good speed, nice screen, keyboard... hard to go wrong"
# {'LAPTOP': ['GREAT'], 'SPEED': ['GOOD'], 'SCREEN': ['NICE']}

# txt = "this laptop has not been great....good speed, nice screen, keyboard... hard to go wrong"
# {'LAPTOP': ['NOT GREAT'], 'SPEED': ['GOOD'], 'SCREEN': ['NICE']}

# txt = "this laptop and PC has not been great, good or not nice."  # we do not double negate the nots in sentences like this
# {'PC': ['GOOD', 'NOT NICE', 'NOT GREAT'], 'LAPTOP': ['GOOD', 'NOT NICE', 'NOT GREAT']}

# txt = "this laptop and PC has not been great, good or nice." 
# {{'PC': ['NOT NICE', 'NOT GOOD', 'NOT GREAT'], 'LAPTOP': ['NOT NICE', 'NOT GOOD', 'NOT GREAT']}

# txt = "this laptop and PC has been great, not good and nice." # WRONG
# {'LAPTOP': ['NOT GOOD', 'NOT NICE', 'GREAT'], 'PC': ['NOT GOOD', 'NOT NICE', 'GREAT']}

# txt = "This is not a good idea or a bad one"
# {'IDEA': ['NOT GOOD'], 'ONE': ['BAD']}

# txt = "This is not a good idea or bad"
# {'IDEA': ['NOT GOOD', 'NOT BAD']}

# {'LAPTOP': ['GREAT'], 'SPEED': ['GOOD'], 'SCREEN': ['GOOD', 'NICE'], 'KEYBOARD': ['GOOD'], 'PRICE': ['FABULOUS']}
# {('LAPTOP', 2): ['LAPTOP'], ('SPEED', 8): ['SPEED', 'SCREEN', 'KEYBOARD'], ('SCREEN', 11): ['SCREEN'], ('KEYBOARD', 13): ['KEYBOARD'], ('BACK', 23): ['BACK'], ('LAPTOP', 25): ['LAPTOP'], ('STUDENT', 30): ['STUDENT'], ('CHILD', 32): ['CHILD'], ('LOT', 35): ['LOT'], ('OOMPH', 37): ['OOMPH'], ('PRICE', 41): ['PRICE']}

# txt = "The Sound Quality is great but the battery life is very bad."
# {'QUALITY': ['GREAT'], 'LIFE': ['BAD']}

# txt = "My time and space in Italy were very enjoyable and fun." 
# {'TIME': ['FUN', 'ENJOYABLE'], 'SPACE': ['FUN', 'ENJOYABLE']}

# txt = "My time and space in Italy were not very enjoyable and fun." 
# {'TIME': ['NOT FUN', 'NOT ENJOYABLE'], 'SPACE': ['NOT FUN', 'NOT ENJOYABLE']}

# txt = "The PC is so much better than before it was"
# {'PC': ['GOOD']}

# txt = "I use this product when I am breaking in new shoes. I get new Sperrys all the time and it is so painful the first few weeks trying to break them in, but I put these in the places where it will rub into a blister, and there is no blister! I have also tried other bandaids and this stays on! It molds to the folds of ur skin and becomes a second skin. Great quality and wil continue to keep on buying"
# {'QUALITY': ['GREAT']}

# txt = "I do not know if this computer is good or bad" # what should we do in this case; include both or none ? We include both for now
# {'COMPUTER': ['BAD', 'GOOD']}

# txt = "This can turn a bad computer into a good computer" # hard one, we can either include both adjective or none and I chose to add both 
# {'COMPUTER': ['BAD', 'GOOD']}

# txt = "This is a bad computer"
# {'COMPUTER': ['BAD']}

# txt = "This computer is bad"
# {'COMPUTER': ['BAD']}

if __name__ == "__main__": # if run directly

  txt = "My time and space in Italy were not very enjoyable and not fun." # an example sentence
  unicode_safe_print(aspectBased_sentiment_analysis(txt))
