import json

import psycopg2

from flask_restx import Resource, Namespace

from app import config

from app.utills.paginations import Pagination
from app.utills.parsers import page_parser, search_parser

Drug = Namespace("Drug")


@Drug.route("/")
class DrugList(Pagination, Resource):
    def get(self):

        """Page별 Drug 리스트를 조회한다."""

        limit = self.page_size
        offset = page_parser.parse_args()["page"] * limit

        query = f"SELECT A.drug_exposure_start_datetime, A.drug_exposure_end_datetime, A.visit_occurrence_id, A.person_id, A.drug_concept_id, B.concept_name \
            FROM drug_exposure as A \
            INNER JOIN concept as B ON A.drug_concept_id = B.concept_id \
            ORDER BY A.drug_exposure_start_datetime OFFSET {offset} LIMIT {limit}"

        db = psycopg2.connect(
            dbname=config["db"]["database"],
            user=config["db"]["username"],
            password=config["db"]["password"],
            host=config["db"]["host"],
            port=config["db"]["port"],
        )

        cursor = db.cursor()
        cursor.execute(query)
        drugs = cursor.fetchall()
        cursor.close()
        db.close()

        drugs = json.dumps(drugs, default=str)
        return drugs
