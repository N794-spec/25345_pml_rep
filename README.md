# 25345_pml_rep
Short Summary 

We built a **Performance Management system**, a full-stack application to track income and expenses.

1.  **Technology Stack**:
    * **Frontend**: Streamlit for a user-friendly web interface.
    * **Backend**: Python with the `psycopg2` library.
    * **Database**: PostgreSQL, a powerful and reliable relational database.

2.  **Code Structure**:
    * We organized the code into three separate files for clarity and maintainability:
        * `table_creation.sql`: To define the database structure.
        * `backend.py`: To handle all database logic (CRUD operations).
        * `frontend.py`: To manage the user interface.

3.  **Key Features**:
    * **CRUD Functionality**: Users can **C**reate (add), **R**ead (view), and **D**elete transactions.
    * **Business Intelligence**: An automated "Insights" section that calculates key metrics like total income/expense, net savings, and average transaction amount using SQL aggregate functions (`COUNT`, `SUM`, `AVG`, etc.).
    * **ACID Compliance**: We confirmed that the system is fully ACID compliant, ensuring every transaction is **A**tomic, **C**onsistent, **I**solated, and **D**urable, which is essential for financial data integrity.
