Initialize env

```
env\Scripts\activate.bat

source env/bin/activate
```

Start server

```
source env/bin/activate && cd website && python manage.py runserver
```

Clone Project

```
Remove existing env directory if it exists.
```

Create requirements.txt file if it doesn't already exist.

```
pipreq .

python3 -m  pipreqs.pipreqs .
```

Create new env folder

```
python -m venv env
```

Install requirements.txt

```
pip install -r requirements.txt
```