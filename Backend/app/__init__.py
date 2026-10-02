# app/__init__.py
from flask import Flask
from flask.globals import request
from config import Config
from app.extensions import db, migrate
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins=app.config["FRONTEND_ORIGINS"],supports_credentials=True)
    @app.before_request
    def log_origin():
        print("Incoming Origin header:", repr(request.headers.get("Origin")))

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import data  # ensures all models are registered for migrations

    from app.routes.schoolRoutes import schools_bp
    from app.routes.gradesRoute import grades_bp
    from app.routes.teachersRoute import teachers_bp
    from app.routes.subjectsRoute import subjects_bp
    from app.routes.subjectRequirementsRoute import requirements_bp
    from app.routes.resourcesRoute import resources_bp
    from app.routes.periodsRoute import periods_bp
    from app.routes.teacherAssignmentRoute import assignments_bp
    from app.routes.optionBlockRoute import option_blocks_bp
    from app.routes.teachersConstraintsRoute import constraints_bp
    from app.routes.timetableRoute import timetable_bp
    from app.routes.auth import auth_bp
    from app.routes.requirementOverviewRoute import requirements_overview_bp
    from app.routes.assignmentFlatRoute import assignments_flat_bp
    from app.routes.constraintOverviewRoute import constraints_overview_bp
    from app.routes.optionGroupAssignmentRoute import option_group_assignments_bp
    for bp in [
        schools_bp, grades_bp, teachers_bp, subjects_bp, requirements_bp,
        resources_bp, periods_bp, assignments_bp, option_blocks_bp,
        constraints_bp, timetable_bp, auth_bp, requirements_overview_bp, assignments_flat_bp,constraints_overview_bp, 
        option_group_assignments_bp,
    ]:
        app.register_blueprint(bp)

    return app