from anime import app


@app.route("/", methods=["GET"])
def welcome():
    return "Welcome to Anime Kaze"
