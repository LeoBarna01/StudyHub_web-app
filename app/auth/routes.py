from flask import (
    render_template, redirect, url_for,
    flash, request
)
from flask_login import (
    current_user, login_user,
    logout_user, login_required
)
from urllib.parse import urlparse
from app import db
from app.auth import bp
from app.auth.form import (
    LoginForm, RegistrationForm,
    EditProfileForm
)
from app.models import User, Document


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login. Redirect authenticated users to home."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # Prevent open‐redirect
            if not next_page or urlparse(next_page).netloc:
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    """Log the user out and redirect to the home page."""
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration. Redirect to login after success."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You may now sign in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Display and allow edits to the current user's profile.
    Also load their uploads and favorites for listing.
    """
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        # Update user fields
        current_user.first_name = form.first_name.data
        current_user.last_name  = form.last_name.data
        current_user.institute  = form.institute.data
        current_user.course     = form.course.data
        current_user.year       = form.year.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))

    # Load user's uploaded documents
    my_uploads = current_user.documents.order_by(
        Document.upload_date.desc()
    ).all()

    # Load user's favorites (requires you to have defined the relationship)
    favorites = current_user.favorites.all()

    return render_template(
        'auth/profile.html',
        form=form,
        my_uploads=my_uploads,
        favorites=favorites
    )