from flask_restx import reqparse

page_parser = reqparse.RequestParser()
page_parser.add_argument("page", type=int)

search_parser = reqparse.RequestParser()
search_parser.add_argument("keyword")
search_parser.add_argument("page")

category_parser = reqparse.RequestParser()
category_parser.add_argument("category")
