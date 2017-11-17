# About Cog

Cog is an efficient, user friendly web application where you can visualize your schedule on a 12-hour time wheel. It automatically estimates the lengths of your tasks and arranges them for you on a unique Donut UI (12-hour time wheel) instead of the classic Google Calendars grid format. Now, you can see how long your tasks will take and make maximum use of your time!

Scheduling itself is a stressful process. Let Cog take care of it for you.

View our initial MVP here: https://cog-tasks.herokuapp.com/
Future Vision: To become a simplistic pooling of many information sources with crowdsourced expandability.

# Cog Instruction Document

Currently our main code is stored in one app. By the Django documentation, one should keep things in a single app as long as they follow the same purpose, and currently all do.

The main app is Dashboard. In future, as other supplementary apps are added, this document will be updated.

Make sure to create a virtual environment and install pip packages using "pip install -r requirements.txt". If you add new requirements, add it using "pip freeze > requirements.txt"

Also need client_secret.json and settings.

```
npm install -g bower
python manage.py bower install
```
