Skillset and Job Portal
Technology Stack: Front end: HTML,CSS and Bootstrap (for Mobile first design model). Backend: Python, Flask, SQLALCHEMY(ORM'S) is used on SQLITE Database.

# Depereceated
# This App is deployed on heroku cloud and is live, and the website url is given below: You can instantly create a user in signup, and signin to the app to use it.

User passwords are encrypted and stored, and OpenSSL is used for secure connection.

To run the app locally, Follow the below instructions. (Make sure python and pip are preinstalled in local)

Clone the repository to local.
Create a Virtual environment in the repo using the below command. "py -m venv venv"
Activate the Virtual Environment using the below command. "venv\scripts\activate" 4.All the needed packages are listed in requirements.txt file, Run the below command to install all the needed libraries in one command. "pip install -r requirements.txt"
After installing the libraries, Start the flask app using "flask run" command.
The flask app will be started and running in your designated local host.
This Application allows user to signup with email-id, password and a secret key. Secret key is used to login, when the password is forgetten. Once logged in, it takes you to the home page, where you can post comments and view other user's comments. The filter module is implemented for displaying only the logged in user's comments, Additionally we can filter other users's comments too, and also reset the filters.

