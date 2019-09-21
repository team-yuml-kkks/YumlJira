[![Build Status](https://travis-ci.com/team-yuml-kkks/YumlJira.svg?)](https://travis-ci.com/team-yuml-kkks/YumlJira/)

# YUML JIRA
JIRA by TEAM YUML

## INSTALLATION

### Prerequisites
```
Python 3.7
Node 10
```

### VIRTUALENV
```
virtualenv env --python=python3
source env/bin/activate
pip install -r requirements/local.txt
```

### MIGRATIONS
First copy `db.base.py` into `db.py` then execute:
```
./manage.py migrate
```

### JAVASCRIPT
```
npm install
npm run build / npm run watch
```

### RUNNING TESTS
```
pytest
npm test
```

### GOOGLE LOGIN
To configure Google Auth you have to add new record to SocialApp model with Google provider
and insert there project keys.

### Default avatar credit
<div>Icon made from <a href="http://www.onlinewebfonts.com/icon">Icon Fonts</a> is licensed by CC BY 3.0</div>

## Authors
Kaniak
Kamil Supera


