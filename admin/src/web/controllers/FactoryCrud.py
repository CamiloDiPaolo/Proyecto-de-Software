from src.core.db import db_session

def get_all_docs_json(Model):
    json = []
    result = db_session.query(Model).all()
    for row in result:
        json.append(row.json())
    return json

def get_doc_json(Model, doc_id):
    result = db_session.query(Model).filter_by(id = doc_id).all()
    for row in result:
        return row.json()
    return {}

def create_doc_json(Model, data):
    # TODO: hashear la contraseña
    # TODO: sanitizar los parametros
    new_doc = Model(data)
    db_session.add_all([new_doc])
    db_session.commit()
    return new_doc.json()

def update_doc_json(Model, doc_id, data):
    # TODO: hashear la contraseña
    # TODO: sanitizar los parametros
    result = db_session.query(Model).filter_by(id = doc_id).all()
    updated_doc = result[0]
    updated_doc.update(data)
    db_session.commit()
    return updated_doc.json()

def delete_doc_json(Model, doc_id):
    result = db_session.query(Model).filter_by(id = doc_id).all()
    for row in result:
        db_session.delete(row)
        db_session.commit()
    return {}
