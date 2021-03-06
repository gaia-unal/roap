
"""
Contains necessary Resources to works with learning-object metadata
fields CRUD operations.
"""

import json
from uuid import uuid4
from datetime import datetime

from marshmallowjson.marshmallowjson import Definition
from marshmallowjson.exceptions import ValidationError
from utils.req_to_dict import req_to_dict
from utils.auth import Authenticate
from utils.switch_language import SwitchLanguage
from bson.json_util import dumps

import falcon


@falcon.before(SwitchLanguage())
class LearningObjectMetadata(object):
    """Deal with the whole collection of learning-object-metadata-fields."""

    def __init__(self, db):
        """Init."""
        self.db = db

    @falcon.before(Authenticate())
    def on_get(self, req, resp):
        """Get a single learning-object-metadata-field."""
        user = req.context.get('user')

        # TODO: view as nested schema or layer nested schema.

        result = list(
            self.db.lom_schema.find().sort("created", -1).limit(1)
        )
        lom = result[0].get('lom')
        full_nested_lom_schema = Definition(lom).to_full_nested()
        result[0]['lom'] = full_nested_lom_schema

        if not result:
            resp.status = falcon.HTTP_404
        else:
            resp.body = dumps(result[0])
            resp.status = falcon.HTTP_200

    @falcon.before(Authenticate())
    def on_post(self, req, resp):
        """Update learning-object-metadata-field."""
        user = req.context.get('user')
        _ = user.get('language')
        if user.get('role') != 'administrator':
            raise falcon.HTTPUnauthorized(_('Only administrator.'))

        lom = req_to_dict(req)
        try:
            Definition(lom)
            result = self.db.lom_schema.insert_one(
                {
                    '_id': str(uuid4()),
                    'lom': lom,
                    'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
            )
            if not result.acknowledged:
                resp.status = falcon.HTTP_400
            else:
                resp.status = falcon.HTTP_201
        except ValidationError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps({'message': json.dumps(e.args[0])})
