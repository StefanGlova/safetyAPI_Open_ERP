from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgres://stefan:JQUVYy4Jmht5CW1Jho50e21b5MNrWErw@dpg-ckatkd6smu8c738por20-a.frankfurt-postgres.render.com/open_erp_database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)


class IncidentModel(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)
    incident_type = db.Column(db.String(20), nullable=False)
    person_name = db.Column(db.String(100), nullable=False)
    incident_date = db.Column(db.Date, nullable=False)
    incident_time = db.Column(db.Time, nullable=False)
    witness_name = db.Column(db.String(100), nullable=False)
    weather = db.Column(db.String(50), nullable=False)
    light = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(
        self,
        incident_type,
        person_name,
        incident_date,
        incident_time,
        witness_name,
        weather,
        light,
        description,
    ):
        self.incident_type = incident_type
        self.person_name = person_name
        self.incident_date = incident_date
        self.incident_time = incident_time
        self.witness_name = witness_name
        self.weather = weather
        self.light = light
        self.description = description

    @validates("incident_type")
    def validate_incident_type(self, incident_type):
        if incident_type not in ("injury", "damage", "near_miss"):
            raise ValueError(
                "Invalid input. Choose from 'injury', 'damage', 'near_miss'"
            )
        return incident_type

    @validates("weather")
    def validate_weather(self, weather):
        if weather not in ("sunny", "rain", "snow", "frizing"):
            raise ValueError(
                "Invalid input. Choose from 'sunny', 'rain', 'neasnowr_miss', 'frizing'"
            )
        return weather

    @validates("light")
    def validate_weather(self, light):
        if light not in ("dark", "ligh inside", "light outside"):
            raise ValueError(
                "Invalid input. Choose from 'dark', 'ligh inside', 'light outside'"
            )
        return light


incident_model = api.model(
    "Incident",
    {
        "id": fields.Integer(readonly=True),
        "incident_type": fields.String(required=True),
        "person_name": fields.String(required=True),
        "incident_date": fields.Date(required=True),
        "incident_time": fields.String(equired=True),
        "witness_name": fields.String(required=True),
        "weather": fields.String(required=True),
        "light": fields.String(required=True),
        "description": fields.String(required=True),
    },
)


@api.route("/incidents")
class IncidentsResource(Resource):
    @api.doc("list_incidents")
    def get(self):
        """
        Get a list of all incidents.
        """
        incidents = IncidentModel.query.all()
        return [
            {
                "id": incident.id,
                "incident_type": incident.incident_type,
                "person_name": incident.person_name,
                "incident_date": incident.incident_date,
                "incident_time": incident.incident_time,
                "witness_name": incident.witness_name,
                "weather": incident.weather,
                "light": incident.light,
                "description": incident.description,
            }
            for incident in incidents
        ]

    @api.doc("record_incident")
    @api.expect(incident_model)
    def post(self):
        """
        Record a new incident.
        """
        args = api.payload
        new_incident = IncidentModel(
            id=args["id"],
            incident_type=args["incident_type"],
            person_name=args["person_name"],
            incident_date=args["incident_date"],
            incident_time=args["incident_time"],
            witness_name=args["witness_name"],
            weather=args["weather"],
            light=args["light"],
            description=args["description"],
        )
        db.session.add(new_incident)
        db.session.commit()
        return {"message": "Incident recorded successfully"}, 201


@api.route("/incidents/<int:id>")
class IncidentResource(Resource):
    """
    Represents a single incident record.
    """

    @api.doc("get_incident")
    def get(self, id):
        """
        Get incident by id.
        """
        incident = IncidentModel.query.get(id)
        if not incident:
            return {"error": "Incident not found"}, 404

        return {
            "id": incident.id,
            "incident_type": incident.incident_type,
            "person_name": incident.person_name,
            "incident_date": incident.incident_date,
            "incident_time": incident.incident_time,
            "witness_name": incident.witness_name,
            "weather": incident.weather,
            "light": incident.light,
            "description": incident.description,
        }

    @api.doc("update_incident")
    @api.expect(incident_model)
    def put(self, id):
        """
        Update an incident by id.
        """
        args = api.payload
        incident = IncidentModel.query.get(id)
        if not incident:
            return {"error": "Incident not found"}, 404

        incident.id = args["id"]
        incident.incident_type = args["incident_type"]
        incident.person_name = args["person_name"]
        incident.incident_date = args["incident_date"]
        incident.incident_time = args["incident_time"]
        incident.witness_name = args["witness_name"]
        incident.weather = args["weather"]
        incident.light = args["light"]
        incident.description = args["description"]

        db.session.commit()
        return {"message": "Incident updated successfully"}, 201

    @api.doc("delete_incident")
    def delete(self, id):
        """
        Delete an incident by id.
        """
        incident = IncidentModel.query.get(id)
        if not incident:
            return {"error": "Incident not found"}, 404
        db.session.delete(incident)
        db.session.commit()
        return {"message": "Incident deleted successfully"}, 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
