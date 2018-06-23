
# /usr/bin/env python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sys
from PyDictionary import PyDictionary

app = Flask(__name__)
dictionary = PyDictionary()
quiz_sessions = {} # Maps: {phone number : (inQuiz, quiz_name, location, num_answers_per_question, num_questions, num_correct)}
                   # Right now we only store one quiz/location per phone number, so a user cannot simultaneously be taking multiple quizzes.

def definition(message_body):
    '''
    Accesses definition from user query.
    '''
    response = ""
    word = message_body.split()[1][:1].upper() + message_body.split()[1][1:]
    word[0].upper()
    definition_entry = dictionary.meaning(message_body.split()[1].lower())
    response = ""
    for key in definition_entry:
        response += word + " (" + key + ")" + ": \n"
        for i in range(0, len(definition_entry[key])):
            response += "(" + str(i+1) + ") " + definition_entry[key][i] + "." + "\n"
    return response

def multiple_choice_quiz(number, message_body):
    response = ""

    if number in quiz_sessions.keys():

        # Then we have a stored session for this number - retrieve that data
        # print(quiz_sessions[number], file=sys.stderr)
        quiz_name = quiz_sessions[number][1]
        location = quiz_sessions[number][2]
        num_answers = quiz_sessions[number][3]
        num_questions = quiz_sessions[number][4]
        num_correct = quiz_sessions[number][5]

        quiz_file = open(quiz_name + ".quiz", "r")
        # Skip the first *location* number of lines in the quiz
        for i in range(location):
            quiz_file.readline()

        # Evaluate whether the answer was correct
        correct_answer = quiz_file.readline()
        location += 1

        if message_body.split()[0].upper() == correct_answer[0]:
            num_correct += 1
        response_feedback = "Correct!" if message_body.split()[0].upper() == correct_answer[0] else "Incorrect. Correct answer was " + correct_answer
        response += response_feedback + "\n"

        # Read through the file, generate our next question
        next_question = quiz_file.readline() # Read in the next question
        last_pos = quiz_file.tell()
        location += 1
        testpos = quiz_file.readline()
        if next_question == testpos:
            # Quiz is over - we have reached our EOF
            try:
                del quiz_sessions[number]
            except KeyError:
                pass
            return response + "The quiz is now over. You scored " + str(num_correct) + "/" + str(num_questions) + ". Thank you for participating!"
        else:
            # Rewind one line from our testpos read
            quiz_file.seek(last_pos)
        response += "Next question:\n"
        response += next_question


        for i in range(num_answers+1):
            response += quiz_file.readline()
            location += 1

        quiz_file.close()
        quiz_sessions[number] = (True, quiz_name, location, num_answers, num_questions+1, num_correct)

    else:
        # Then we don't have a stored session for this phone number
        location = 0
        quiz_name = message_body.split()[1].lower()
        # Print out the first four lines of the quiz file
        try:
            quiz_file = open(quiz_name + ".quiz", "r")
        except IOError:
            response = "The quiz you have attempted to access, " + message_body.split()[1] + ", does not appear to exist in our database. Please double check the quiz name and try again."
            return response

        num_answers = int(quiz_file.readline())
        location += 1

        # Welcome message
        response += "Welcome to the quiz!\n"

        response += quiz_file.readline() + "\n" # Read in the question
        location += 1

        for i in range(num_answers):
            # Read in the answers
            response += quiz_file.readline()
            location += 1

        quiz_file.close()

        # Save our data to the quiz_sessions dictionary
        num_questions = 0
        num_correct = 0
        quiz_sessions[number] = (True, quiz_name, location, num_answers, num_questions, num_correct)

    return response

def process_user_request(number, message_body):

    user_command = message_body.split()[0].lower()

    if user_command == "define":
        # Then we know that it is a dictionary query - pass request to dictionary function
        resp_string = definition(message_body)

    elif user_command == "quiz" or quiz_sessions[number][0]:
        # Then we know the user either wants to start a new quiz, or has a current
        # quiz session open.
        resp_string = multiple_choice_quiz(number, message_body)

    return resp_string
        

@app.route("/sms", methods=['POST'])
def sms_response():
    # Start our response
    
    number = request.form['From']
    message_body = request.form['Body']

    # print(request.form, file=sys.stderr)
    resp = MessagingResponse()

    resp_string = process_user_request(number, message_body)

    # Add a message
    resp.message(resp_string)

    return str(resp)
    #return resp_string

def testing_mode():

    test_number = "+15555555555"
    
    while(True):
        response = ""
        PROMPT_COLOR = '\033[92m' # This is a green colour on my UNIX terminal
        PROMPT_BOLD = '\033[1m'
        PROMPT_END = '\033[0m'
        user_input = input(PROMPT_COLOR + PROMPT_BOLD + "[SMS] >> " + PROMPT_END)
        
        if user_input.lower() == "quit" or user_input.lower() == "exit":
            break

        response = process_user_request(test_number, user_input)

        print(response)

    print("Exiting test suite")
    return

if __name__ == "__main__":

    if len(sys.argv) == 1:
        # Then we have no extra arguments - run the serverside normally
        app.run(debug=True)
    
    elif len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        # Then run the server in testing mode
        testing_mode()




