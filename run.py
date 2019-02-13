from flask import Flask

from api.v2 import create_app

env = "development"

app = create_app(env)



if __name__ == "__main__":
    app.run()
