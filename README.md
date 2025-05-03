# CITS3403_GROUP_PROJECT

## What is "Who is Free?"
*Who is Free?* is a powerful tool in the fast paced and often all too busy world of today. Access your calendar anywhere, with no need to share data across platforms!

Your calendar is stored securely and privately, allowing you to share exactly the parts of your schedule you want with other users. 
Add your contacts and establish share groups, so your poker table doesn't have to see your work meetings.

Use our analytical tools to track when you are most busy across the week to plan out your time better. Match up your calendar with your friends and see when the best time to meet will be!

## Who Are We?

### Group_gc_91
| Student Number | Name             | GitHub user   |
| -------------- | ---------------- | ------------- |
| 23067779       | Dennis Lou       | ls-woozie     |
| 23208949       | Sunyan Qin       | SunyanQin9527 |
| 24149594       | Nam Tran         | namhai2307    |
| 22262964       | Alistair Langton | langtonic     |


### How to run "Who is Free?"
1. Unzip or clone the app data onto your local device
`git clone namhai2307/CITS3403_GROUP_PROJECT`
2. Ensure all required packages are installed
`pip install -r requirements.txt`
3. Initialise the databases
``` 
flask db init
flask db migrate -m "Initial user table"
flask db migrate -m "Events Table"
flask db upgrade
```
5. Run the application on your localhost
`flask run`

### How to run the tests
