from flask import render_template
from . import bp
@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Handle 404 errors: page not found.
    """
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors: internal server error.
    """
    return render_template('errors/500.html'), 500
