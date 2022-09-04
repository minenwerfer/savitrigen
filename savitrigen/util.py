from functools import reduce

ts_type_mapping = {
    'string': [
        'text',
        'textarea',
        'string',
        'select',
        'checkbox',
        'radio'
    ],
    'number': [
        'number',
        'integer'
    ],
    'ObjectId': [
        'collection',
        'objectid'
    ],
    'boolean': 'boolean',
    'Date': 'datetime',
    'any': 'object',
}

def extract_collection(field:dict) -> str:
    def extract_query(value:dict) -> dict:
        return value.get('__query', None) \
            if type(value) is dict else None

    is_array = field.get('array', False)

    if collection := field.get('collection'):
        return collection, is_array

    if values := field.get('values'):
        if query := extract_query(
            values
            if not isinstance(field['values'], list)
            else field['values'][0]
        ):
            return (
                query['collection'],
                is_array or isinstance(field['values'], list)
            )

def extract_collections(fields:dict) -> str:
    for k, v in fields.items():
        _tuple = extract_collection(v)
        if _tuple:
            yield _tuple

def convert_type(name:str) -> dict:
    t = next((
        k
        for k, v in ts_type_mapping.items()
        if name in v
    ), None)

    if not t:
        raise Exception('unknown type "{}"'.format(name))

    return t

def map_fields(fields:dict) -> dict:
    def reducer(a:dict, item:tuple) -> dict:
        k, v = item
        field_type = v.get('type', 'text')

        _tuple = extract_collection(v)
        if _tuple:
            collection, is_array = _tuple
            type_name = '{}Document'.format(collection[0].upper() + collection[1:])
            if is_array:
                type_name = 'Array<{}>'.format(type_name)
            return a | { k: type_name }

        return a | { k: convert_type(field_type) }
    return reduce(reducer, fields.items(), {})

def make_ts_typehints(obj:dict) -> str:
    def reducer(a:str, item:tuple) -> list:
        k, v = item
        return a + ["  {}: {}".format(k, v)]
    return "\n".join(reduce(reducer, obj.items(), []))

