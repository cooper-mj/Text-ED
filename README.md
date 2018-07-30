# Text-ED
An SMS Education Platform.

## Getting Started
Welcome to the Text-ED project! Thank you for stopping by.

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Text-ED requires Python 3.4 or later. If you are running an older version of Python, [download the latest version here](https://www.python.org/downloads/).

The following installation instructions assume a familiarity running commands in a Terminal. __If you are unfamiliar with running commands on a terminal, there are two conventions to keep in mind__ when following the below instructions: (1) The ```$``` sign is a convention indicating that the following command is a command to be run in Terminal; do not include it when actually running your commands. (2) Square brackets are used to indicate variable information that you should include without the square brackets. For example, if a command says, ```$ cd [project_folder]```, the real command would look something like ```$ cd Text-ED``` depending on the name of the project folder and your current location in your computer's file tree.

### Installation

1. Download the git repository to your computer:
```
$ git clone [project_url]
```

2. Install libraries

Navigate to the newly-created project folder in your Terminal, and run the following command to install the necessary pip dependencies:
```
$ pip install -r requirements.txt
```

3. Run the server on your machine

Use the following command to run the server in test mode on your machine:

```
$ python3 serverside.py test
```
After running this command, you should see the following prompt appear in your terminal:

<span style="color:green">__```[SMS] >>```__</span>

At which point you are running the serverside software in test mode. Test mode enables you to locally run the serverside software to test commands without running it remotely on a server linked to a Twilio account. To exit this prompt (and return to your normal terminal), you can type either ```quit()``` or ```exit()``` at the <span style="color:green">__```[SMS] >>```__</span> prompt.

[comment]: <> ### Orientation


## Deployment

[comment]: <> TODO: instructions on getting setup with Twilio, running this using their platform, and ngrok.

## Built With

* [Twilio](https://www.twilio.com/)
* [Flask](http://flask.pocoo.org/)

## Contributing

If you wish to contribute to this project, we would welcome your support!

To offer feedback and ideas, please open an issue in the GitHub repository, or send me an email. 

## Authors

Current active developers: 

* [Michael Cooper](https://github.com/cooper-mj)

## License

## Acknowledgments

