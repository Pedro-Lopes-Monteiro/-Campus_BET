from flask import Blueprint

profile_bp = Blueprint("profile", __name__, template_folder="../../templates/profile", url_prefix="/perfil")

from . import routes

