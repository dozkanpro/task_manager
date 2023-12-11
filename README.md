# Introduction
This is a task manager website which required login process. 
There are 3 task status: proposed, in progress and completed.
   
|Task Status |Usage | Flash Messages |
| :-:        | :-: |  :-: |
|Proposed    |Only Administrator can add a new task into the database.|"Task added successfully"|
|In progress |Any authenticated user can start a task. Status in the task is changed in the database. |"Task started successfully" |
|Completed  |Any authenticated user can complete a task. Status in the task is changed in the database. |"Task completed successfully" |


## Getting Started
- **Fork the repository:** You should **fork the repository** and then **clone it** so you can manage your own repo and use this only as a template.
  ```
  $ git clone https://github.com/your_username/your-project.git
  ```
- **Install dependencies:**

  ```
  pip install -r requirements.txt
  ```
- **Change** 'SECRET_KEY' with your **own**.

## Endpoints
|Route |Usage |
| :-:  | :-: |
|`/ `  | For list all tasks in the database if only user is authenticated.|
|`/register`  | For register new user into database.|
|`/login`  | For login user.|
|`/logout`  | For logout user.|
|`/tasks`  | For adding a new task into the database. If only user is admin.|
|`/start_task/<int:task_id>`  | For start a task.|
|`/complete_task/<int:task_id>`  | For complete a task.|


## Features
- Python
- Flask
- flask_bootstrap
- flask_wtf
- flask_sqlalchemy
- wtforms
- flask_login
  
## **How to login works?:** 
1. When you:
    1. sign-up, password is hashed and salted, then stored in the database.
    2. sign-in, hashed-salted password is compared to the password in the database.
2. If the hashes password:
    1. match, you are logged in.
    2. don't match, you are not logged in.
3. If user already exist:
   1. Flash message is shown: "You've already signed up with that email, log in instead!"
   2. Redirect to '/login'.
4. If login is succesfull:
   1. Redirect to '/get_all_tasks'. 
       
