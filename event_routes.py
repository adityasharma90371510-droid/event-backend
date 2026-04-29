# event_event_routes_final_event_system

from flask import Blueprint, request, jsonify
from event_models import db, Client
from event_utils import save_to_excel, load_banned_words, load_guest_names, normalize_text

api_bp = Blueprint('api', __name__)


# ----------------------------------------
# SUBMIT NAME (MAIN ENTRY API)
# ----------------------------------------
@api_bp.route('/submit-name', methods=['POST'])
def submit_name():
    data = request.get_json()
    name = data.get("name", "").strip()

    # -----------------------
    # VALIDATION
    # -----------------------
    if not name:
        return jsonify({"error": "Name required"}), 400

    # 🔥 FULL NAME CHECK (ADDED)
    if len(name.split()) < 2:
        return jsonify({"error": "Please enter your full name"}), 400

    # LENGTH CHECK
    if len(name) < 2 or len(name) > 50:
        return jsonify({"error": "Name must be 2-50 characters"}), 400

    # -----------------------
    # NORMALIZE TEXT
    # -----------------------
    cleaned = normalize_text(name)

    # -----------------------
    # ABUSE FILTER
    # -----------------------
    banned_words = load_banned_words()

    for word in banned_words:
        if word in cleaned:
            return jsonify({
                "error": "sorry this contains a banned phrase/word"
            }), 400

    # -----------------------
    # DUPLICATE CHECK (REMOVED LOGIC BUT STRUCTURE KEPT)
    # -----------------------
    # NOTE: Duplicate restriction removed for event flow
    # if Client.query.filter_by(name=name).first():
    #     return jsonify({"error": "Name already entered"}), 400

    # -----------------------
    # LIMIT CHECK (MAX 500)
    # -----------------------
    if Client.query.count() >= 500:
        return jsonify({"error": "Max limit reached"}), 400

    # -----------------------
    # SAVE
    # -----------------------
    client = Client(name=name)

    db.session.add(client)
    db.session.commit()

    # -----------------------
    # SAVE TO EXCEL
    # -----------------------
    save_to_excel(client.to_dict())

    return jsonify({
        "message": "Name submitted successfully"
    })


# ----------------------------------------
# GET NAMES (FOR DIYA DISPLAY)
# ----------------------------------------
@api_bp.route('/get-names', methods=['GET'])
def get_names():

    names = [c.name for c in Client.query.all()]

    # -----------------------
    # MIN 100 LOGIC
    # -----------------------
    if len(names) < 100:
        guest_list = load_guest_names()

        for g in guest_list:
            if g not in names:
                names.append(g)

            if len(names) >= 100:
                break

    return jsonify({
        "names": names[:500]
    })


# ----------------------------------------
# RESET (OPTIONAL FOR TESTING)
# ----------------------------------------
@api_bp.route('/reset', methods=['POST'])
def reset_data():
    db.session.query(Client).delete()
    db.session.commit()

    return {"message": "All data cleared"}