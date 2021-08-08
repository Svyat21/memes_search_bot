from config import el_search


def add_to_index(index, model):
    if not el_search:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    el_search.index(index=index, doc_type=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not el_search:
        return
    el_search.delete(index=index, doc_type=index, id=model.id)


def query_index(index, query, page, per_page):
    if not el_search:
        return [], 0
    search = el_search.search(
        index=index, doc_type=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']
