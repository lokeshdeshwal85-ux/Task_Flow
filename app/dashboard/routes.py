from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Project, Task, User, ProjectMember

dashboard_bp = Blueprint("dashboard", __name__)


def build_task_chart_data(tasks, projects=None):
    pending_tasks = len([task for task in tasks if task.status == "Pending"])
    progress_tasks = len([task for task in tasks if task.status == "In Progress"])
    completed_tasks = len([task for task in tasks if task.status == "Completed"])

    low_priority = len([task for task in tasks if task.priority == "Low"])
    medium_priority = len([task for task in tasks if task.priority == "Medium"])
    high_priority = len([task for task in tasks if task.priority == "High"])
    critical_priority = len([task for task in tasks if task.priority == "Critical"])

    chart_data = {
        "status_labels": ["Pending", "In Progress", "Completed"],
        "status_values": [pending_tasks, progress_tasks, completed_tasks],
        "priority_labels": ["Low", "Medium", "High", "Critical"],
        "priority_values": [low_priority, medium_priority, high_priority, critical_priority],
    }

    if projects is not None:
        chart_data["project_labels"] = [project.title for project in projects]
        chart_data["project_values"] = [project.progress() for project in projects]

    return chart_data, completed_tasks


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin():
        projects = Project.query.order_by(Project.created_at.desc()).all()
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        users = User.query.all()
        overdue = [task for task in tasks if task.is_overdue()]
        chart_data, completed_tasks = build_task_chart_data(tasks, projects)

        return render_template(
            "dashboard/admin_dashboard.html",
            projects=projects,
            tasks=tasks,
            users=users,
            overdue=overdue,
            chart_data=chart_data,
            completed_tasks=completed_tasks
        )

    memberships = ProjectMember.query.filter_by(user_id=current_user.id).all()
    project_ids = [m.project_id for m in memberships]
    projects = Project.query.filter(Project.id.in_(project_ids)).all() if project_ids else []
    tasks = Task.query.filter_by(assigned_to=current_user.id).order_by(Task.created_at.desc()).all()
    overdue = [task for task in tasks if task.is_overdue()]
    chart_data, completed_tasks = build_task_chart_data(tasks, projects)

    return render_template(
        "dashboard/member_dashboard.html",
        projects=projects,
        tasks=tasks,
        overdue=overdue,
        chart_data=chart_data,
        completed_tasks=completed_tasks
    )
