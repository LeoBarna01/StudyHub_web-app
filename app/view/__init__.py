from flask import Blueprint

bp = Blueprint('view', __name__)

from app.view import view, utils
