# To Using BS4 template with flask @ Heroku platform

a easy practice...

## resouce

- [startBootstrap](https://startbootstrap.com/)
- [for demo1, I choose this one](https://startbootstrap.com/template-overviews/creative/)
- [click to download](https://github.com/BlackrockDigital/startbootstrap-creative/archive/gh-pages.zip)

## local test

- prepare "app.py" in root folder "flask_bs4_t0", it's content:

```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__': 
    app.run(debug=True)
```

- unzip "gh-pages.zip", and create "static", "templates" in the root folder
- copy template "gh-pages.zip"'s resource: all folder (css, img, js, scss, vendor) to folder "static"
- copy template "gh-pages.zip"'s resource: "index.html" to folder "templates"

- run `python app.py` and check result with [localhot](http://127.0.0.1:5000), you will see text page only
- modify "index.html":
  - link start with "vendor/" --> "static/vendor/"
  - link start with "css/" --> "static/css/"
  - link start with "vendor/" --> "static/vendor/"
  - link start with "img/" --> "static/img/"
  - link start with "portfolio/" --> "static/portfolio/"
  - and etc... like above...
  
- press "F5" on the browser, you will see all the thing is ready! good!


## push to Heroku

- add a file "Procfile":
```
web: gunicorn app:app --log-file=-
```

- add a file "requirements.txt":
```
flask
flask-cors
gunicorn
Flask-RESTful
Jinja2
```

- using commands as below:
```
git init
git add .
git commit -am "first version"
heroku apps:create my-bs4-app1
git push heroku master
```

- got a good template app @ Heroku! nice! [link](https://my-bs4-app1.herokuapp.com/)


