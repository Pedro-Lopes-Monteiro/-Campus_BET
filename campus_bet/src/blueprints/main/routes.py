from flask import render_template
from flask_login import current_user
from . import main_bp
from src.mock_data import events_mock, sports_mock # Using mock data

@main_bp.route("/")
@main_bp.route("/index")
def index():
    # Pass mock data to the template
    # For simplicity, directly passing some mock events and sports
    # In a real app, you might have more complex logic to select featured events
    featured_events = events_mock[:4]
    return render_template("index.html", title="Início", current_user=current_user, sports=sports_mock, featured_events=featured_events)

@main_bp.route("/search", methods=["GET", "POST"])
def search_results():
    # Mock search functionality
    query = request.form.get("search_query") if request.method == "POST" else request.args.get("query")
    results = []
    if query:
        for event in events_mock:
            if query.lower() in event["name_event"].lower():
                results.append(event)
        for sport in sports_mock:
            if query.lower() in sport["name"].lower():
                # You might want to list events of this sport
                pass 
    return render_template("search_results_mock.html", title=f"Resultados para: {query}", results=results, current_user=current_user)

