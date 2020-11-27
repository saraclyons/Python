**Prerequisite:** 
Python 3, 
Docker

The app was connected to a  local MySQL db

`CREATE TABLE IF NOT EXISTS users(
   email VARCHAR(255) PRIMARY KEY,
   passwd VARCHAR(255) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=INNODB;`


**Run the Application:**

To run the application, enter in your terminal:

`docker build -t registration:v1 .` 

`docker run -dit --rm -p 5000:5000 --name registration registration:v1`

`docker ps` should display the above container 

http://localhost:5000/signup will direct you to the signup page
