# Cog Instruction Document

Currently our main code is stored in one app. By the Django documentation, one should keep things in a single app as long as they follow the same purpose, and currently all do.

The main app is Dashboard. In future, as other supplementary apps are added, this document will be updated.

Make sure to create a virtual environment and install pip packages using "pip install -r requirements.txt". If you add new requirements, add it using "pip freeze > requirements.txt"

Also need client_secret.json and settings.

```
npm install -g bower
python manage.py bower install
```
