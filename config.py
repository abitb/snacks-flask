import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	API_KEY = "a1bacf53-c847-4b5d-81fa-822b8138ecda"

class DevelopmentConfig(Config):
	DATABASE_URI = os.path.join(basedir, "snacks.db")
	# Secret key for session management.
	SECRET_KEY = "This can be generated randomly"

config = {
    "development": DevelopmentConfig
}