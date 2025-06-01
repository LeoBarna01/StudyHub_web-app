from flask import render_template, flash, redirect, url_for, request
from app import db
from app.form import bp
from app.form.forms import QuestionForm
from app.models import Question

@bp.route('/form', methods=['GET', 'POST'])
def ask_question():
    """
    GET:  Render the question form page.
    POST: Validate and process the submitted form.
          Save the question to the database or send notification email.
    """
    form = QuestionForm()
    if form.validate_on_submit():
        # Save question in database
        question = Question(
            subject=form.subject.data,
            email=form.email.data,
            body=form.body.data
        )
        db.session.add(question)
        db.session.commit()

        # Optionally, send notification email here
        flash('Your request has been submitted successfully.', 'success')
        return redirect(url_for('form.ask_question'))

    # On GET or validation failure, render the form
    return render_template('form/question_form.html', form=form)