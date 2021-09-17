import json

import psycopg2

from flask_restx import Resource, Namespace

from app import config

from app.utills.paginations import Pagination
from app.utills.parsers import page_parser

Condition = Namespace("Condition")


@Condition.route("/")
class ConditionList(Pagination, Resource):
    def get(self):

        """Page별 condition 리스트를 조회한다."""

        limit = self.page_size
        offset = page_parser.parse_args()["page"] * limit

        query = f"SELECT A.condition_start_datetime, A.condition_end_datetime, A.visit_occurrence_id, A.person_id, A.condition_concept_id, B.concept_name \
            FROM condition_occurrence as A \
            INNER JOIN concept as B ON A.condition_concept_id = B.concept_id \
            ORDER BY A.condition_start_datetime OFFSET {offset} LIMIT {limit}"

        db = psycopg2.connect(
            dbname=config["db"]["database"],
            user=config["db"]["username"],
            password=config["db"]["password"],
            host=config["db"]["host"],
            port=config["db"]["port"],
        )

        cursor = db.cursor()
        cursor.execute(query)
        conditions = cursor.fetchall()
        cursor.close()
        db.close()

        conditions = json.dumps(conditions, default=str)
        return conditions
