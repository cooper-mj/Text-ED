
# /usr/bin/env python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sys
from PyDictionary import PyDictionary

app = Flask(__name__)
dictionary = PyDictionary()
quiz_sessions = {} # Maps: {phone number : (inQuiz, quiz_name, location, num_answers_per_question, num_questions, num_correct)}
                   # Right now we only store one quiz/location per number

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
        quiz_file = open(quiz_name + ".quiz", "r")
        
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

@app.route("/sms", methods=['POST'])
def sms_response():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    
    number = request.form['From']
    message_body = request.form['Body']

    # print(request.form, file=sys.stderr)
    resp = MessagingResponse()

    if message_body.split()[0].lower() == "define":
        # Then we know that it is a dictionary query - handle request accordingly
        resp_string = definition(message_body)

    if message_body.split()[0].lower() == "quiz" or quiz_sessions[number][0]:
        resp_string = multiple_choice_quiz(number, message_body)
        

    # Now we manipulate the message body accordingly

    # Add a message
    resp.message(resp_string)

    return str(resp)
    #return resp_string
if __name__ == "__main__":
    app.run(debug=True)
    #instr = input("Enter a term: ")
    #print(sms_response(instr))