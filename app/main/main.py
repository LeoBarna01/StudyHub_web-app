
from flask import render_template
from . import bp

@bp.route('/errore')
def errore():
    """
    Pagina di errore generica per i link del footer.
    """
    return render_template('erros/404.html'), 404

@bp.route('/')
def index():
    """
    StudyHub Homepage
    """
    return render_template('main/home.html')