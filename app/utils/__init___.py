from flask import render_template

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template("405.html"), 405

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500
