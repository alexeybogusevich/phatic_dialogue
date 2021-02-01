import stanza 
import random
#stanza.download('en')
nlp = stanza.Pipeline('en')

greetings = [
    'hi',
    'hello',
    'good morning',
    'good afternoon',
    'good evening'
]

greeting_answers = [
    'Hi! How are you?',
    'Hello! How do you do?',
    'Nice to meet you! How is it going?'
]

partings = [
    'bye',
    'goodbye'
]

coincidences = [
    'What a coincidence!',
    'No, really?',
    'The same is true for me!',
    'This is cool!'
]

preferences = [
    'I like',
    'I love',
    'I adore',
    'I am fond of',
    'I\'m fond of',
    'I prefer',
    'I don\'t like',
    'I dislike',
    'I hate',
    'I can\'t stand'
]

person_descriptions = [
    'You are',
    'you are'
]

default_questions = [
    'How are you?',
    'Tell me something!',
    'How was your day?',
    'Tell me something about yourself!',
    'What did you do yesterday?',
    'Who is your hero?',
    'If you could live anywhere, where would it be?',
    'What is your biggest fear?',
    'What is your favorite family vacation?',
    'What would you change about yourself if you could?',
    'What really makes you angry?',
    'What motivates you to work hard?',
    'What is your favorite thing about your career?',
    'What is your biggest complaint about your job?',
    'What is your proudest accomplishment?',
    'What is your child\'s proudest accomplishment?',
    'What is your favorite book to read?',
    'What makes you laugh the most?',
    'What was the last movie you went to? What did you think?',
    'What did you want to be when you were small?',
    'What does your child want to be when he/she grows up?',
    'If you could choose to do anything for a day, what would it be?',
    'What is your favorite game or sport to watch and play?',
    'Would you rather ride a bike, ride a horse, or drive a car?',
    'What would you sing at Karaoke night?',
    'What two radio stations do you listen to in the car the most?',
    'Who is your favorite author?',
    'Have you ever had a nickname? What is it?',
    'Do you like or dislike surprises? Why or why not?' 
    'What\'s the tallest building you\'ve been to the top in?',
    'Would you rather trade intelligence for looks or looks for intelligence?',
    'How many pairs of shoes do you own?',
    'If you were a super-hero, what powers would you have?',
    'What would you do if you won the lottery?',
    'What form of public transportation do you prefer? (air, boat, train, bus, car, etc.)',
    'If you could go back in time to change one thing, what would it be?'
    #... https://www.signupgenius.com/groups/getting-to-know-you-questions.cfm
]

default_answers = [
    'I\'m sorry, but I cannot answer this question.',
    'Can you ask me later?',
    'I did not get it. Let\'s change the subject!',
    'Let\'s talk about it later.'
]

defaut_misunderstandings = [
    'I did not get it. Let\'s change the subject!',
    'I\'m not sure about it. Let\'s change the subject!'
]

primitive_statement_answers = [
    'Well, I see you don\'t talk much.',
    'Don\'t be so shy! Talk more!'
]

verb_questions = [
    'How',
    'When',
    'Where',
    'Why'
]

entity_questions = {
    'TIME':[
        'It can\'t be {}. Are you sure?',
        'Are you sure that the mentioned time is exact (I mean {})?',
    ],
    'GPE':[
        'Have you visited {} in the past?',
        'Oh, what a nice place. What is {} famous for?',
        'Do you know how to get to {}?'
    ],
    'PERSON':[
        'What do you know about {}?',
        'Do you know {} personally?',
        'Do you like {}?',
        'When was {} born?',
        'Where was {} born?',
        'How old is {}?',
        'I have heared about {}. Tell me more about this person.',
             ],
    'ORG':[
        'What do you know about {}?',
        'Is {} a public organization?',
        'Do you know who is the owner of {}?',
        'When was {} founded?'
    ],
    'EVENT':[
        'Is {} a public event?',
        'Who is the organizer of {}?',
        'Where does {} take place?'
    ],
    'DATE':[
        'What else do you know about that date? (I mean {})',
        'Which famous person was born then? (I mean {})',
    ],
    'CARDINAL':[
        'Are you sure that {} is the correct number?'
    ]
}

def process_message(message):
    print('You: ' + message)
    if len(set.intersection(set(message.lower().split()),set(greetings))) > 0:
        process_greetings()
        return
    if len(set.intersection(set(message.lower().split()),set(partings))) > 0:
        process_partings()
        return
    if len(message.split()) < 3:
        process_primitive_answer()
        return
    if '?' in message:
        process_question()
        return
    message_nlp = nlp(message)
    for target_sentence in message_nlp.sentences:
        if any(preference.lower() in target_sentence.text.lower() for preference in preferences):
            process_preferences(target_sentence.text)
            return
        if any(description.lower() in target_sentence.text.lower() for description in person_descriptions):
            process_descriptions(target_sentence.text)
            return
        sentence_entities = target_sentence.entities
        if len(sentence_entities) != 0:
            process_sentence_entities(sentence_entities)
            return
        sentence_root = get_root_dependency(target_sentence.dependencies)
        if sentence_root[2].upos == 'VERB':
            if process_root_verb(sentence_root, target_sentence.dependencies):
                return
    process_finally()

def process_greetings():
    print('Person: ' + random.choice(greeting_answers))
    
def process_partings():
    print('Person: ' + random.choice(partings))

def process_question():
    print('Person: ' + random.choice(default_answers))
    print('Person: ' + random.choice(default_questions))
    
def process_primitive_answer():
    print('Person: ' + random.choice(primitive_statement_answers))
    print('Person: ' + random.choice(default_questions))

def process_preferences(preference_sentence):
    print('Person: ' + random.choice(coincidences) + ' ' + preference_sentence + ' too!')
    return

def process_descriptions(description_sentence):
    print('Person: Thank you! I also think that ' + description_sentence)
    return

def get_root_dependency(dependencies):
    root_dependency = next(d for d in dependencies if d[1] == 'root')
    return root_dependency

def process_root_verb(root_dependency, dependencies):
    verb = root_dependency[2].text
    nsubj_dependencies = list(filter(lambda d: d[1] == 'nsubj', dependencies))
    root_subject_dependencies = list(filter(lambda d: d[0].text == verb or d[2].text == verb, nsubj_dependencies))
    if len(root_subject_dependencies) == 0:
        return False
    subject_dependency = root_subject_dependencies[0]
    if subject_dependency[2].upos == 'VERB':
        subject_text = subject_dependency[0].text
    else:
        subject_text = subject_dependency[2].text
    plural = "Plur" in subject_dependency[0].feats
    if subject_text == 'I':
        subject_text = 'you'
        plural = True
    if 'Past' in root_dependency[2].feats:
        print('Person: ' + random.choice(verb_questions) + ' did ' + subject_text + ' do that?')
        return True
    if 'Present' in root_dependency[2].feats:
        if 'ing' in root_dependency[2].text:
            if are_aux:
                print('Person: ' + random.choice(verb_questions) + ' are ' + subject_text + ' doing that?')
            else:
                print('Person: ' + random.choice(verb_questions) + ' is ' + subject_text + ' doing that?')
        else:
            if plural:
                print('Person: ' + random.choice(verb_questions) + ' do ' + subject_text + ' do that?')
            else:
                print('Person: ' + random.choice(verb_questions) + ' does ' + subject_text + ' do that?')
        return True
    if 'Future' in root_dependency[2].feats:
        print('Person: ' + random.choice(verb_questions) + ' would ' + subject_text + ' do that?')
        return True

def process_sentence_entities(sentence_entities):
    chosen_entity = random.choice(sentence_entities)
    question_list = entity_questions[chosen_entity.type]
    chosen_question = random.choice(question_list)
    print('Person: ' + chosen_question.format(chosen_entity.text))
    
def process_finally():
    print('Person: ' + random.choice(defaut_misunderstandings))
    print('Person: ' + random.choice(default_questions))
    



if __name__ == '__main__':
    print('Welcome to Phatic Chat! Let\'s talk!')
    while(True):
        message = str(input())
        process_message(message)
