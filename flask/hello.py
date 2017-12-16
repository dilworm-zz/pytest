# -*-coding=utf8-*-
from flask import Flask
from flask import request 
from flask import current_app
from flask import make_response
from flask import render_template

app = Flask("gogo")

@app.route("/")
def index():
    user_agent = request.headers.get("User-Agent")
    ret = "hello world is %s\n" % (user_agent)
    ret = ret + "current_app = %s\n"%(current_app.name)
    return ret

@app.route("/oauth/<platform>")
def oauth_platform(platform):
    return "oauth platform %s" % platform

@app.route("/show_url_maps")
def show_url_maps():
    return str(app.url_map), 400

@app.route("/make_response")
def make_response():
    response = make_response('<h1>This is make_response</h1>')
    response.set_cookie("answer", "yes")
    return response

# 使用模板
@app.route("/user/<name>")
def user(name):
    #return render_template('user.html', name=name)
    return render_template('derived.html', name=name, title="88888")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400

if __name__ == "__main__":
    app.run(debug=True)






