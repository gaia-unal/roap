
"""
Contains utility functions to works with learning-object get many.
"""


def get_many(db_client, filter_, range_, sorted_, user, learning_object_format):
    """Get learning objects with query."""

    start, end = range_
    field, order = sorted_

    user_role = user.get('role')
    user_id = user.get('id')

    # Role level permissions
    user_role_permissions_handler = {
        'oai': [
            {'status': 'accepted', 'deleted': {
                '$in': [True, False]
            }}
        ],
        'external': [
            {'status': 'accepted', 'deleted': False},
        ],
        'creator': [
            {
                'creator_id': user_id,
                'status': {
                    '$in': ['pending', 'evaluated', 'accepted', 'rejected']
                }
            },
            {'status': 'accepted', 'deleted': False},
        ],
        'expert': [
            {
                'expert_ids': user_id,
                'status': {
                    '$in': ['pending', 'evaluated', 'accepted', 'rejected']
                }
            },
            {
                'creator_id': user_id,
                'status': {
                    '$in': ['pending', 'evaluated', 'accepted', 'rejected']
                }
            },
            {'status': 'accepted', 'deleted': False}
        ],
        'administrator': [
            {}
        ],
    }

    initial_query = {'$or': user_role_permissions_handler.get(user_role)}

    if filter_.get('q'):
        query = {'$text': {
            '$search': filter_.get('q'),
            '$diacriticSensitive': False,
            '$caseSensitive': False,
        }}
        query = {**initial_query, **query}
        cursor = db_client.learning_objects.find(
            query
        )
        learning_objects = list(
            cursor
            .skip(start)
            .limit((end - start) + 1)
        )
    else:
        query = {**initial_query, **filter_}
        cursor = db_client.learning_objects.find(query)
        learning_objects = list(
            cursor
            .sort([(field, -1 if order == 'DESC' else 1)])
            .skip(start)
            .limit((end - start) + 1)
        )

    if learning_object_format:
        format_handler = {
            'xml': lambda lo: lo.get('metadata_xml'),
        }
        for index_lo in range(len(learning_objects)):
            learning_objects[index_lo]['metadata'] = format_handler[learning_object_format](
                learning_objects[index_lo])

    return learning_objects, cursor.count()
