# RESTful Application for Patient Clinical Data Collection and Reporting

Here are the user storeis below for the application(in agile methodology)

## User Story: 1
**As a lab assistant, I want to view all the patient records**
#### Acceptance Criteria
 - Display all the patients’ details with their id, firstName, lastName and age
 - Display the link to enter clinical data for each patient
 - Display the link to analyse data for each patient
 - Display the link to register new patients

## User Story: 2
**As a lab assistant, I want to register a new patient**
#### Acceptance Criteria
 - On Click of the Add Patient link the user should be navigated to the patient registration screen
 - The user should see a form that he can fill in with patient details namely firstName, lastName, and age
 - When the user click the confirm button the data should be saved and a conformation message should be displayed
 - The user should be able to navigate back to the home page

## User Story: 3
**As a lab assistant, I want to enter clinical data for a patient**
#### Acceptance Criteria
 - On click of the Add Data link on the home page the user should be navigated to the clinical data entry screen
 - The user should see a form that he can fill in with patient details such as BP or Height and Weight or or Heart rate
 - When the user click the confirm button the data should be saved and a confirmation message should be displayed
 - The user should be able to navigate back to the home screen




## User Story: 4
**As a lab assistant, I want to analyse and see a report of the latest tests**
#### Acceptance Criteria
 - On click of the Analyse Data link on the home page the user should be navigated to page where he can see the latest entries for various clinical data
 - The body mass index should be displayed based on height and weight of the patient 
 - The user should see a link to a graph that will show the clinical regarding on a line chart over time


### Steps to run the App
 - install the packages in requirements.txt file (cmd : **pip install -r requirements.txt**)
 - create database : **clinicalsdb** and add configuration details in DATABASES section in settings.py file
 - apply migrations (cmd : **python manage.py makemigrations**)
 - run migrations (cmd : **python manage.py migrate**)
 - run the app (cmd : **python manage.py runserver**)
