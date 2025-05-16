# CITS3403_GROUP_PROJECT

## What is "Who is Free?"

*Who is Free?* is a powerful tool in the fast paced and often all-too-busy world of today.

Access your calendar anywhere, with no need to share data across platforms!  

Your calendar is stored securely and privately, allowing you to share exactly the parts of your schedule you want with other users.  

Add your contacts and establish share groups, so your poker table doesn’t have to see your work meetings.

Use our analytical tools to track when you are most busy across the week to plan out your time better. Match up your calendar with your friends and see when the best time to meet will be!

## Who Are We?

### Group_gc_91

| Student Number | Name             | GitHub user   |
| -------------- | ---------------- | ------------- |
| 23067779       | Dennis Lou       | ls-woozie     |
| 23208949       | Sunyan Qin       | SunyanQin9527 |
| 24149594       | Nam Tran         | namhai2307    |
| 22262964       | Alistair Langton | langtonic     |

## How to run "Who is Free?"

1. **Unzip or clone the app data onto your local device**:  
   ```bash
   git clone https://github.com/namhai2307/CITS3403_GROUP_PROJECT.git
2. **Create a Virtual Environment**
   **For MacOS/Linux:**
   ```bash
   python -m venv venv 
   source venv/bin/activate
   ```
   **For Windows:**
   ```bash
   python -m venv venv 
   .\venv\Scripts\Activate.ps1
   ```
   Once activated the terminal prompt should shoul (venv).
2. **Installing the necessary packages**
   ```bash
   pip install -r requirements.txt
   ```
3. **Initalise the database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
4. **Setting up your own secret key to run the web app in your local environment**
  
   ***Note**: Make sure to replace the "your-production-secret-key" to your own secret key message.
   
   **For MacOS/Linux:**
   ```bash
   export SECRET_KEY='your-production-secret-key'
    ```
   
   **For Windows:**
   ```bash
   $env:SECRET_KEY = "your-production-secret-key"
   ```
   

5. Run the application on your localhost
   ```bash
   flask run

## How to run the test?
   ***Note**: Make sure you have the flask server running up first, then call these commands to run the tests. <br>
   **For Unit Tests:**
   ```bash
   python -m unittest app.unit_test
   ```
   **For Selenium Tests:**
   ```bash
   python -m unittest app.selenium_test
   ```

*Disclaimer: This project consists the use of AI, specifically Github Copilot as part of our references.


