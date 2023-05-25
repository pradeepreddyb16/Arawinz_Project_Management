from flask import Flask,Blueprint
from pytz import timezone
from models.admin_models import models as db


api=Blueprint('api',__name__,url_prefix='/api')