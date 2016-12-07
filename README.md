# adi-twitter

This repository is part of the subject 'Aplicaciones distribuidas en internet'

the goals of this work are:
- Learn how to communicate with a REST API
- Use OAuth to authenticate an user
- Use Twitter API to create a simple client that performs actions such as tweeting, deleting tweets and follow user
- Use Jinja2 as a templating system.
- Use CSS to improve the readaility of the page
- Use flashing to show feedback to the user

How to run the project:
- Clone the project: 

`git clone https://github.com/JCepedaVillamayor/adi-twitter.git`
- Connect to Twitter API and create an app ([Follow these Steps](https://iag.me/socialmedia/how-to-create-a-twitter-app-in-8-easy-steps/))
- Create a virtualenv:

`virtualenv -p /usr/bin/python2.7 venv`
- Activate the virtualenv:

`source venv/bin/activate`
- Copy the consumer and private key obtained from your app and add it to your environment variables 
(add the environment variables to `venv/bin/postactivate`)
- Install the requirements:

`pip install -r requirements.txt`
- Execute the app:

`python manage.py runserver`
