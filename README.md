# 25345_pml_rep
Short Summary 

This project is a simple, web-based *Performance Management System* built with Python and PostgreSQL. It's designed to help managers and employees track goals and performance.


### `tables.sql`
This script sets up your PostgreSQL database. It creates the necessary tables to store information about:
* **Goals**: For tracking employee objectives.
* **Tasks**: The specific actions needed to complete goals.
* **Feedback**: For managers' comments on performance.
It also includes an automated trigger to send a "well done" message when a goal is marked as complete.



### `backend.py`
This is the engine of the application. It handles all the logic and communication with the database. Key functions include:
* Connecting to the PostgreSQL database.
* CRUD (Create, Read, Update, Delete)** operations for managing goals, tasks, and feedback.
* A function to generate **business insights**, such as counting completed goals and calculating the average number of tasks per goal.

***

### `frontend.py`
This file creates the user interface using the Streamlit library, making it interactive and easy to use. It provides:
* A Manager View**: Where managers can create and update goals, approve tasks, and leave feedback.
* An Employee View**: Where employees can see their assigned goals, add tasks, and view feedback.
* A Business Insights** section to display key performance metrics from the backend.
