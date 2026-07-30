import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

from app.core.config import settings


# Load HTML templates
BASE_DIR = Path(__file__).resolve().parent.parent

templates = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates")
)


def render_template(
    template_name: str,
    **context
):
    template = templates.get_template(template_name)
    return template.render(**context)


def send_email(
    to_email: str,
    subject: str,
    body: str,
    html: str | None = None
):
    """
    Generic email sender.
    """

    message = MIMEMultipart("alternative")

    message["From"] = f"{settings.FROM_NAME} <{settings.SMTP_EMAIL}>"
    message["To"] = to_email
    message["Subject"] = subject

    # Plain text version
    message.attach(MIMEText(body, "plain"))

    # HTML version
    if html:
        message.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(
            settings.SMTP_SERVER,
            settings.SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                settings.SMTP_EMAIL,
                settings.SMTP_PASSWORD
            )

            server.send_message(message)

        print(f"Email sent to {to_email}")
        return True

    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def send_ticket_created_email(
    employee_email: str,
    employee_name: str,
    ticket_title: str
):
    subject = "Ticket Created Successfully"

    body = f"""Hello {employee_name},

Your ticket has been created successfully.

Title: {ticket_title}

Thank you,
HospitalAI Help Desk
"""

    html = render_template(
        "ticket_created.html",
        employee_name=employee_name,
        ticket_title=ticket_title
    )

    return send_email(
        employee_email,
        subject,
        body,
        html
    )


def send_ticket_assigned_email(
    engineer_email: str,
    engineer_name: str,
    ticket_title: str,
    ticket_description: str,
    priority: str,
    department: str,
    assigned_by: str
):
    subject = "New Ticket Assigned"

    body = f"""Hello {engineer_name},

A new ticket has been assigned to you.

Title: {ticket_title}
Department: {department}
Priority: {priority}

Description:
{ticket_description}

Assigned By:
{assigned_by}

Please review and resolve it as soon as possible.

HospitalAI Help Desk
"""

    html = render_template(
        "ticket_assigned.html",
        engineer_name=engineer_name,
        ticket_title=ticket_title,
        ticket_description=ticket_description,
        priority=priority,
        department=department,
        assigned_by=assigned_by
    )

    return send_email(
        engineer_email,
        subject,
        body,
        html
    )


def send_ticket_resolved_email(
    employee_email: str,
    employee_name: str,
    ticket_title: str
):
    subject = "Ticket Resolved"

    body = f"""Hello {employee_name},

Your ticket has been resolved.

Title: {ticket_title}

Thank you for using HospitalAI Help Desk.
"""

    html = render_template(
        "ticket_resolved.html",
        employee_name=employee_name,
        ticket_title=ticket_title
    )

    return send_email(
        employee_email,
        subject,
        body,
        html
    )


def send_comment_notification(
    employee_email: str,
    employee_name: str,
    ticket_title: str,
    comment: str
):
    subject = "New Comment on Your Ticket"

    body = f"""Hello {employee_name},

A new comment has been added to your ticket.

Ticket: {ticket_title}

Comment:
{comment}

Please log in to HospitalAI to view the latest update.

HospitalAI Help Desk
"""

    html = render_template(
        "comment_notification.html",
        employee_name=employee_name,
        ticket_title=ticket_title,
        comment=comment
    )

    return send_email(
        employee_email,
        subject,
        body,
        html
    )