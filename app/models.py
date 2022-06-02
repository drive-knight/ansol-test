from app import db
from sqlalchemy.dialects.postgresql import ARRAY



class Document( db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    rubrics = db.Column(ARRAY(db.String(255)), nullable=False, index=False)
    text = db.Column(db.String(), index=False, nullable=False)
    created_date = db.Column(db.String(255), nullable=False, index=False)

    def __repr__(self):
        return f'{self.text}'