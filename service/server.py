from flask import Flask

from service.apis.geozones import geozones

app = Flask(__name__, static_folder="openapi")

blueprints_to_add = (geozones,)
for blueprint in blueprints_to_add:
    url_prefix = f"/{blueprint.name}"
    app.register_blueprint(blueprint, url_prefix=url_prefix)


@app.route("/")
def greeting():
    """Test root endpoint"""
    return "This is a delivery app. Enjoy"


if __name__ == "__main__":
    app.run(debug=True, port=80, host="localhost")
