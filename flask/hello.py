from flask import Flask
app = Flask("gogo")

@app.route("/")
def hello():
    return "hello world"

@app.route("/oauth/<platform>")
def oauth_platform(platform):
    return "oauth platform %s" % platform

if __name__ == "__main__":
    app.run()
