import json

import psycopg2

from flask_restx import Resource, Namespace

from app import config

from app.utills.paginations import Pagination
from app.utills.parsers import page_parser


Concept = Namespace("Concept")


@Concept.route("/")
class ConceptList(Pagination, Resource):
    @Concept.doc("Concept List")
    def get(self):

        """Page별 concept 리스트를 조회한다."""
        limit = self.page_size
        offset = page_parser.parse_args()["page"] * limit

        query = f"SELECT concept_id, concept_name, domain_id FROM concept OFFSET {offset} LIMIT {limit}"

        db = psycopg2.connect(
            dbname=config["db"]["database"],
            user=config["db"]["username"],
            password=config["db"]["password"],
            host=config["db"]["host"],
            port=config["db"]["port"],
        )

        cursor = db.cursor()
        cursor.execute(query)
        concepts = cursor.fetchall()
        cursor.close()
        db.close()

        concepts = json.dumps(concepts, default=str)
        return concepts
