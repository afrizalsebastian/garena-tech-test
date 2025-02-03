# GARENA BACKEND TEST

## Requirements

<li><strong>PYHTON</strong></li>
<li><strong>MYSQL</strong></li>
<li><strong>REDIS SERVER</strong></li>

## Setup Project

<ol>
  <li>Start mysql serivce</li>
  <li>Make a new database in mysql</li>

```bash
mysql -u root -p
```

```sql
CREATE DATABASE <database_name>;
```

  <li>Install libraries used in project in requirements.txt</li>

```bash
pip install -r ./requirements.txt
```

  <li>Start Redis Server</li>

```bash
redis-server
```

&nbsp;&nbsp;&nbsp;or run it in the background services

  <li>Make the .env file</li>
  Duplicate the <strong>.env.example</strong> and customize the SECRET_KEY, DATABASE, and REDIS_URL
</ol>

## Run the project

Use command below to run the project

```bash
python manage.py runserve
```

or

```bash
python3 manage.py runserve
```

## Documentation

Use can use the [json file documentation postman](documentation.postman.json) or use the [postman app](https://www.postman.com/descent-module-engineer-54466928/workspace/public/collection/29345756-3c101fd8-d1f5-4ce8-983b-a1d633d77dc8?action=share&creator=29345756&active-environment=29345756-651a13ea-a4fa-451c-9d51-b143bf5c33c2)
