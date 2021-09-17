import json
import psycopg2

from flask_restx import Resource, Namespace

from app import config

from app.utills.parsers import category_parser

Person = Namespace("Person")


@Person.route("/stats")
class PersonStats(Resource):
    queries = {
        "gender": f"SELECT B.concept_name as gender, COUNT(A.person_id) as count \
            FROM person as A, concept as B \
            WHERE A.gender_concept_id=B.concept_id GROUP BY A.gender_concept_id, B.concept_id",
        "race": f"SELECT B.concept_name as race, COUNT(A.person_id) as count \
            FROM person as A, concept as B \
            WHERE A.race_concept_id=B.concept_id GROUP BY A.race_concept_id, B.concept_id",
        "ethnicity": f"SELECT B.concept_name as ethnicity, COUNT(A.person_id) as count \
            FROM person as A, concept as B \
            WHERE A.ethnicity_concept_id=B.concept_id GROUP BY A.ethnicity_concept_id, B.concept_id",
        "death": "SELECT COUNT(person_id) as count FROM death",
    }

    def get(self):
        query = "SELECT COUNT(person_id) as count FROM person"
        category = category_parser.parse_args()["category"]

        if category:
            query = self.queries[category]

        db = psycopg2.connect(
            dbname=config["db"]["database"],
            user=config["db"]["username"],
            password=config["db"]["password"],
            host=config["db"]["host"],
            port=config["db"]["port"],
        )

        cursor = db.cursor()
        cursor.execute(query)
        persons = cursor.fetchall()
        cursor.close()
        db.close()

        response = json.dumps(persons, default=str)
        return response
