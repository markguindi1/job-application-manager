# job-application-manager

This project is a web application that allows the user to manage their job applications in an easy and simple way. The app integrates with the user's email account, allowing the user to connect certain emails and email threads with job applications, allowing the user to view all the jobs they have applied for (or, are planning to apply for), as well as all emails relevant to that job application. 

This app is a personal project that I'm working on over the summer of 2018, to further develop my programming and web developemnt skills, and in particular using the Django web framework. 

The web app uses Python 3.6, the Django Web Framework (version 2.0), and a PostgreSQL database backend. Styles are done using Bootstrap. 

This project is still in development. So far, the following have been completed:
* Allowing a user to create, edit, and delete job applications, and their relevant information
* Allowing the user to log into their Gmail account (without using OAuth2, so "Enable less secure apps" must be enabled on their account), retrieve messages from their inbox since a specified date, and view the message sender, subject, and date received, in a table.
* User registration, login, authentication, and logout
  
I hope to add the following functionalities soon, as I work on this project over the summer of 2018:
* User registration, and further user account functions (password reset, etc.)
* Linking user's multiple email accounts, so they only need to provide a password for authentication
* Support for email accounts other than Gmail
* Secure authentication using OAuth2 & Google APIs
* Linking emails to job applications, as noted above
* Managing appointments (interviews, meetings, etc.) related to job applications

I hope to utilize standard Python/Django tools, such as Class-Based-Views, and perhaps third-party libraries for easy HTML-table-generation, and email management libraries, so users can use this project as an example for their Django projects. 
