from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import profile_bp
from src.models import User

@profile_bp.route("/")
@login_required
def view_my_profile():
    # Exibe o perfil do usuário autenticado
    return render_template("view_profile.html", user=current_user)

@profile_bp.route("/<string:username>")
@login_required
def view_user_profile(username):
    # Busca usuário pelo username no banco de dados
    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f"Perfil para o usuário {username} não encontrado.", "warning")
        return redirect(url_for("main.index"))
    is_own_profile = (current_user.id == user.id)
    return render_template("view_profile.html", user=user, is_own_profile=is_own_profile)

@profile_bp.route("/editar", methods=["GET", "POST"])
@login_required
def edit_profile():
    # Aqui você pode implementar a edição do perfil real futuramente
    flash("Funcionalidade de edição de perfil ainda não implementada.", "info")
    return redirect(url_for("profile.view_my_profile"))

# Need a simple template for edit_profile.html
# This should be created in templates/profile/edit_profile.html

