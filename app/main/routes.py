from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import Document
import jinja2
from app import db
from app import es


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/search', methods=('GET', 'POST'))
@main.route('/', methods=('GET', 'POST'))
def index():
    q = request.form.get('q') or request.args.get('q')
    docs = []
    if q is not None:
        response = es.search(index='text', body={'query': {'match': {'text': q}}}, size=20, sort={'id': {'order': 'asc'}})
        for r in response['hits']['hits']:
            docs.append(Document.query.filter_by(id=r['sort'][0]).first())
        return render_template('index.html', q=q, docs=docs)
    return render_template('index.html')


@main.route('/delete/<int:doc_id>', methods=['POST'])
def delete(doc_id):
    try:
        doc = Document.query.get_or_404(doc_id)
        es.delete_by_query(index='text', body={'query': {'match': {'id': doc_id}}})
        db.session.delete(doc)
        db.session.commit()
        flash('Документ успешно удален')
    except jinja2.exceptions.UndefinedError:
        pass
    finally:
        return redirect(url_for('main.index'))




