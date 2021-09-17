import json

import psycopg2

from flask_restx import Resource, Namespace

from app import config

from app.utills.parsers import category_parser

Visit = Namespace("Visit")


@Visit.route("/stats")
class VisitStats(Resource):
    queries = {
        "gender": "SELECT C.concept_name, COUNT(A.visit_occurrence_id) as count \
            FROM visit_occurrence as A \
            INNER JOIN person as B ON A.person_id=B.person_id \
            INNER JOIN concept as C ON B.gender_concept_id=C.concept_id \
            GROUP BY B.gender_concept_id, C.concept_id",
        "race": "SELECT C.concept_name, COUNT(A.visit_occurrence_id) as count \
            FROM visit_occurrence as A \
            INNER JOIN person as B ON A.person_id=B.person_id \
            INNER JOIN concept as C ON B.race_concept_id=C.concept_id \
            GROUP BY B.race_concept_id, C.concept_id",
        "ethnicity": "SELECT C.concept_name, COUNT(A.visit_occurrence_id) as count \
            FROM visit_occurrence as A \
            INNER JOIN person as B ON A.person_id=B.person_id \
            INNER JOIN concept as C ON B.ethnicity_concept_id=C.concept_id \
            GROUP BY B.ethnicity_concept_id, C.concept_id",
    }

    def get(self):
        query = "SELECT B.concept_name, COUNT(visit_occurrence_id) as count \
            FROM visit_occurrence as A, concept as B WHERE A.visit_concept_id=B.concept_id \
            GROUP BY A.visit_concept_id, B.concept_id"
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
        reqponse = cursor.fetchall()
        cursor.close()
        db.close()

        reqponse = json.dumps(reqponse, default=str)
        return reqponse
