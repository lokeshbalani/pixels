# PIXELS - Interactive Image Processing WebApp

Interactive web application for demonstrating digital image processing techniques.

## Instructions : Running the Webapp (without `virtualenv`)
```bash
git clone https://github.com/lokeshbalani/pixels.git
```

```bash
cd pixels
```

```bash
pip install -r requirements.txt
```

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```

## Instructions : Running the Webapp (on `virtualenv`)
```bash
git clone https://github.com/lokeshbalani/pixels.git
```

```bash
cd pixels
```

```bash
virtualenv py_env
```

```bash
source py_env/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```

When done deactivate/terminate the virtual environment
```bash
deactivate
```

To install and setup python virtual environment refer to the below URL:  
https://docs.python-guide.org/dev/virtualenvs/







## TODO
* Make modules (extendable)
* In*teractive usable in classroom
* Intermediate steps
* IIIT Virtual Labs - Image Processing Lab
* Saving Image