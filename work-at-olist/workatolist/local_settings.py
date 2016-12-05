import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'BATATA'
DATABASES = {
    'default': dj_database_url.parse("postgres://jhjmycyxwayjla:LuOKQbd23yowUDQO0NUhpPSUSs@ec2-54-246-82-155.eu-west-1.compute.amazonaws.com:5432/dck1lgf56nksel")
}
