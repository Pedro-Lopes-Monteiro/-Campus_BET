from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
import datetime

from . import bets_bp
from src.forms import BetSubmissionForm
from src.mock_data import get_open_bets_by_user_id, get_resolved_bets_by_user_id, events_mock, odds_mock, bets_mock, users_mock # Using mock data

@bets_bp.route("/minhas")
@login_required
def my_bets():
    user_id = int(current_user.get_id()) # Ensure user_id is int for mock_data functions
    open_bets_data = get_open_bets_by_user_id(user_id)
    resolved_bets_data = get_resolved_bets_by_user_id(user_id)
    return render_template("my_bets.html", title="Minhas Apostas", 
                           open_bets=open_bets_data, 
                           resolved_bets=resolved_bets_data, 
                           current_user=current_user)

@bets_bp.route("/fazer-aposta/<int:event_id>", methods=["GET", "POST"])
@login_required
def place_bet(event_id):
    event = next((e for e in events_mock if e["id"] == event_id), None)
    if not event:
        flash("Evento não encontrado.", "danger")
        return redirect(url_for("main.index"))

    # Get odds for this event to populate the form
    event_odds = [odd for odd in odds_mock if odd["event_id"] == event_id]
    
    form = BetSubmissionForm()
    # Corrigir a atribuição de choices
    choices_list = []
    for odd in event_odds:
        tipo_odd = odd["tipo_odd"]
        valor_odd = odd["valor_odd"]
        choices_list.append((odd["id"], f"{tipo_odd} ({valor_odd})"))
    form.selected_odd_id.choices = choices_list

    if form.validate_on_submit():
        user_id = int(current_user.get_id())
        user = next((u for u in users_mock if u["id"] == user_id), None)
        selected_odd_data = next((o for o in odds_mock if o["id"] == form.selected_odd_id.data), None)
        amount = form.amount_staked.data

        if not user or not selected_odd_data:
            flash("Erro ao processar a aposta. Tente novamente.", "danger")
            return redirect(url_for("bets.place_bet", event_id=event_id))

        if user["saldo"] < amount:
            flash("Saldo insuficiente para realizar esta aposta.", "warning")
            return redirect(url_for("bets.place_bet", event_id=event_id))

        # Simulate placing the bet
        user["saldo"] -= float(amount) # Deduct from balance
        new_bet_id = len(bets_mock) + 1
        
        # Usar selected_odd_data para obter tipo_odd e valor_odd
        bet_type_str = selected_odd_data["tipo_odd"]
        odd_value_float = selected_odd_data["valor_odd"]
        event_name_str = event["name_event"]
        sport_name_str = event["sport_name"]

        new_bet = {
            "id": new_bet_id,
            "user_id": user_id,
            "event_id": event_id,
            "event_name": event_name_str,
            "sport_name": sport_name_str,
            "odd_id": selected_odd_data["id"],
            "bet_type": bet_type_str,
            "valor_apostado": float(amount),
            "odd_value": odd_value_float,
            "potential_return": float(amount) * odd_value_float,
            "amount_won": None,
            "data_aposta": datetime.datetime.now(),
            "status": "Aberta",
            "date_resolved": None
        }
        bets_mock.append(new_bet)
        flash(f"Aposta de R$ {amount} em 	{bet_type_str}	 para o evento 	{event_name_str}	 realizada com sucesso!", "success")
        return redirect(url_for("bets.my_bets"))

    # For GET request, or if form validation fails
    event_name_for_title = event["name_event"]
    return render_template("place_bet_mock.html", title=f"Apostar em: {event_name_for_title}", 
                           form=form, event=event, event_odds=event_odds, current_user=current_user)

# Need a simple template for place_bet_mock.html
# This should be created in templates/bets/place_bet_mock.html

