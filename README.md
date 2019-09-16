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
```

## Authors
Kaniak
Kamil Supera


