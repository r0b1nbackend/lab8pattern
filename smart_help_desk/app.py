from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from patterns.commands import (
    AddTicketCommand,
    DeleteTicketCommand,
    ResolveTicketCommand,
)
from patterns.mediator import HelpDeskMediator


# ==================================================
# FLASK APPLICATION
# ==================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = "classroom-demo-key"

mediator = HelpDeskMediator()


@app.get("/")
def index():
    query = request.args.get("filter", "all")
    error = None

    try:
        tickets = mediator.get_tickets(query)
    except ValueError as exc:
        tickets = mediator.get_tickets("all")
        error = str(exc)

    return render_template(
        "index.html",
        tickets=tickets,
        current_filter=query,
        error=error,
    )


@app.post("/add")
def add_ticket():
    command = AddTicketCommand(
        request.form.get("title", ""),
        request.form.get("description", ""),
        request.form.get("category", ""),
    )

    try:
        command.execute(mediator)
        flash("Ticket added successfully.", "success")
    except ValueError as exc:
        flash(str(exc), "error")

    return redirect(url_for("index"))


@app.post("/resolve/<int:ticket_id>")
def resolve_ticket(ticket_id: int):
    success = ResolveTicketCommand(ticket_id).execute(mediator)

    if success:
        flash("Ticket marked as resolved.", "success")
    else:
        flash("Ticket was not found.", "error")

    return redirect(url_for("index"))


@app.post("/delete/<int:ticket_id>")
def delete_ticket(ticket_id: int):
    success = DeleteTicketCommand(ticket_id).execute(mediator)

    if success:
        flash("Ticket deleted.", "success")
    else:
        flash("Ticket was not found.", "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
