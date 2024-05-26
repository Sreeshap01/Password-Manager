# Password Manager
### Video Demo:  https://www.youtube.com/watch?v=uIhXmMvMeic
#### The Password Manager application allows users to manage the usernames and passwords of various sites.This project is inspired by google password manager. It's built using  HTML, CSS and JavaScript in the front end,and Python with flask and SQLite database  in the backend.

#### **Registration :**
The users  should first register in the application via _Register_ page.This page has three fields:User name, Password and Password Confirmation. Password should meet the following criteria:
at least 1 letter, at least 1 number, and a minimum of eight characters.The password and the password confirmation should match.User name, Password and Password Confirmation are mandatory to submit this page._Register_ uses ***register.html*** to render the page, ***/register*** flask route and ***scripts_register.js*** to validate the password criteria.The password criteria is validated in the backend by Python code as well. The password is hashed using Werkzeug library.

#### **Log In :**
The registered users  can log in to the application using their user name and password._Log in_ uses ***login.html*** to render the page, ***/login*** flask route to validate the user name and password.

#### **Index page :**
The index page displays the saved  data of the user(Site URL and Nick Name) in a tabular format. User can navigate to other features from the index page such as adding new site details, viewing the saved data details, change password and log out._Index_ uses ***index.html***  and ***/*** route.

#### **Change Password :**
The change password page allows the user to change the saved password for the application login.This page has three fields, old password, new password and the password confirmation. Password should meet the following criteria: at least 1 letter, at least 1 number, and a minimum of eight characters.The password and the password confirmation should match.Old Password, Password and Password Confirmation are mandatory to submit this page.._Change Password_ uses ***changepassword.html***  and ***/changepassword*** route.**scripts_register.js*** is used to validate the password criteria.The password criteria is validated in the backend by Python code as well. The password is hashed using Werkzeug library.

#### **Add site details :**
The Add button on the index page takes user to the page where the login details of a site are entered.
The following fields are available: Site URL,nick name, user name, password and password confirmation.
.All fields other than the nick name are mandatory. Site URL should be unique.The passwords of the sites are encrypted using cryptography library. _Add_ uses ***addpassword.html***  and ***/addpassword*** route.***scripts_addpassword.js*** is used by this page to use the JavaScript function to return to the index page on clicking the cancel button.

#### **View details :**
From the index page , user can open the details of the specific site in a read-only mode by clicking on the Site URL or the nick name.The following fields are displayed in the detail: Site URL, nick name and user name .From this view, user can modify the specific site data or delete it or can go back to the index page._View details_ uses ***detail.html***  and ***/detail/<id>*** route.

#### **Modify details :**
The modify link allows the user to modify any of the saved information of the specific site.This includes Site URL, nick name, user name, password and password confirmation. The same rules as those of adding a new site are applied while modifying as well.The passwords are encrypted and decrypted using cryptography library . _Modify_ uses ***modify.html***  and ***/modify/<id>*** route.***scripts_modifypassword.js*** is used by this page to use the JavaScript function to return to the detail page on clicking the cancel button.

#### **Delete details :**
The delete button on click displays a confirmatory message, selecting OK to which the data is deleted . This pop up message is displayed by using JavaScript functions and it uses a delete method in the ***/delete/<id>*** route to delete the entry from the database.


#### **Log out :**
The ***/logout*** route is used to log the user out of the application.

The logo(***logo.png***) and icon(***favicon.ico***) files used in this application are downloaded from the internet.

All the CSS used by this application are from ***styles.css** file.***app.py*** contains all the routes.***passmanager.db*** is the database.***requirements.txt*** contains the list of the python packages required for this application.***helpers.py*** contains all the helper functions.***apology.html*** contains the template for error messages.***layout.html*** contains the common structure of all the web pages in this application.
