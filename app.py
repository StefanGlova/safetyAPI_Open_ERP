from flask import Flask, request, jsonify
from models import db, Incident
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://stefan:JQUVYy4Jmht5CW1Jho50e21b5MNrWErw@dpg-ckatkd6smu8c738por20-a.frankfurt-postgres.render.com/open_erp_database"
db.init_app(app)

@app.route("/add_entry", methods=["POST"])
def add_entry():
    try:
        data = request.json
        incident = Incident(
            incident_type=data.get("incident_type")
            incident_date=data.get("incident_date")
            person_name=data.get("person_name")
            description=data.get("description")
        )
        db.session.add(incident)
        db.session.commit()
        return jsonify({"message": "Incident added successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Incident report failed. Check your data"}), 400
    

@app.route("/view_entry/<int:entry_id>", methods=["GET"])
def view_entry(entry_id):
    incident = Incident.query.get(entry_id)
    if incident:
        return jsonify({
            "id": incident.id,
            "incident_type": incident.incident_type,
            "incident_date": incident.incident_date.isoformat(),
            "person_name": incident.person_name,
            "description": incident.description            
        })
    else:
        return jsonify({"error": "Incident not found"}), 404
