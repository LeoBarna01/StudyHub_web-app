from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.forum import bp
from app.models import Group, GroupPost, GroupReply, GroupJoinRequest, User, Notification
from app.forum.forms import CreateGroupForm, CreatePostForm, CreateReplyForm
import string
import random
from datetime import datetime
from werkzeug.utils import secure_filename
import os

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Display all groups the user has access to or search for a group by code."""
    search_code = request.args.get('group_code')
    searched_group = None

    if search_code:
        # Find group by code
        searched_group = Group.query.filter_by(group_code=search_code.upper()).first()
        if not searched_group:
            flash(f'No group found with code: {search_code}', 'warning')

    # Get groups where user is a member (only if not searching or search failed to find a group)
    user_groups = []
    other_groups = []
    if not searched_group:
        user_groups = current_user.groups.all()

        user_member_ids = [member.id for member in current_user.groups.all()]
        other_groups = Group.query.filter(
            Group.is_private == False,
            ~Group.members.any(User.id == current_user.id)
        ).all()

    return render_template('forum/index.html',
                           user_groups=user_groups,
                           other_groups=other_groups,
                           searched_group=searched_group,
                           search_code=search_code)

def generate_group_code():
    """Generates a unique 5-character alphanumeric code."""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        # Check if code is unique
        existing_group = Group.query.filter_by(group_code=code).first()
        if not existing_group:
            return code

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_group():
    """Create a new study group."""
    form = CreateGroupForm()
    if form.validate_on_submit():
        group = Group(
            name=form.name.data,
            description=form.description.data,
            is_private=form.is_private.data,
            created_by=current_user,
            # Generate and assign the group code
            group_code=generate_group_code()
        )
        group.members.append(current_user)
        
        db.session.add(group)
        db.session.commit()
        flash('Group created successfully!', 'success')
        return redirect(url_for('forum.view_group', group_id=group.id))
    
    return render_template('forum/create_group.html', form=form)

@bp.route('/group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def view_group(group_id):
    """View a specific group and its posts."""
    group = Group.query.get_or_404(group_id)
    
    # Check if user has access
    if group.is_private:
        if group not in current_user.groups:
            flash('You do not have access to this group.', 'danger')
            return redirect(url_for('forum.index'))
    
    # Fetch and order posts
    posts = GroupPost.query.filter_by(group_id=group.id).order_by(GroupPost.created_at.desc()).all()
    
    reply_form = CreateReplyForm()
    if reply_form.validate_on_submit() and request.method == 'POST':
        post_id = request.form.get('post_id')
        post_to_reply = GroupPost.query.get(post_id)
        if post_to_reply:
            reply = GroupReply(
                content=reply_form.content.data,
                post=post_to_reply,
                author=current_user
            )
            db.session.add(reply)
            # Create notification if the replier is not the post author
            if post_to_reply.author != current_user:
                notification = Notification(
                    user_id=post_to_reply.author_id,
                    type='new_reply',
                    message=f'{current_user.first_name} {current_user.last_name} replied to your post "{post_to_reply.title}" in group "{post_to_reply.group.name}"',
                    related_resource_id=post_to_reply.id,
                    related_resource_type='GroupPost'
                )
                db.session.add(notification)
            db.session.commit()
            flash('Your reply has been posted!', 'success')
        else:
            flash('Could not find the post to reply to.', 'danger')
        
        return redirect(url_for('forum.view_group', group_id=group.id))

    return render_template('forum/view_group.html',
                         group=group,
                         posts=posts,
                         reply_form=reply_form)

@bp.route('/group/<int:group_id>/join')
@login_required
def join_group(group_id):
    """Join a public group."""
    group = Group.query.get_or_404(group_id)
    
    if group.is_private:
        flash('Cannot join private groups directly.', 'danger')
        return redirect(url_for('forum.index'))
    
    # Check if already a member
    if group in current_user.groups:
        flash('You are already a member of this group.', 'info')
    else:
        group.members.append(current_user)
        db.session.commit()
        flash('Successfully joined the group!', 'success')
    
    return redirect(url_for('forum.view_group', group_id=group.id))

@bp.route('/group/<int:group_id>/post', methods=['GET', 'POST'])
@login_required
def create_post(group_id):
    """Create a new post in a group."""
    group = Group.query.get_or_404(group_id)
    
    # Check if user is a member
    if group.is_private and group not in current_user.groups:
        flash('You must be a member to post in this group.', 'danger')
        return redirect(url_for('forum.index'))
    
    form = CreatePostForm()
    if form.validate_on_submit():
        filename = None
        if form.file.data:
            file = form.file.data
            filename = secure_filename(file.filename)
            # Ensure the upload directory exists
            upload_folder = os.path.join(bp.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

        post = GroupPost(
            title=form.title.data,
            content=form.content.data,
            filename=filename, # Store the filename
            group=group,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('forum.view_group', group_id=group.id))
    
    return render_template('forum/create_post.html',
                         form=form,
                         group=group)

@bp.route('/group/<int:group_id>/request_join')
@login_required
def request_join_group(group_id):
    """Handles requests to join a private group."""
    group = Group.query.get_or_404(group_id)

    # Ensure the group is private
    if not group.is_private:
        flash('This group is not private and can be joined directly.', 'warning')
        return redirect(url_for('forum.index'))

    # Check if user is already a member
    if group in current_user.groups:
        flash('You are already a member of this group.', 'info')
        return redirect(url_for('forum.view_group', group_id=group.id))

    # Check if a pending request already exists
    existing_request = GroupJoinRequest.query.filter_by(
        group_id=group.id,
        user_id=current_user.id,
        status='pending'
    ).first()
    if existing_request:
        flash('You have already sent a request to join this group.', 'info')
        return redirect(url_for('forum.index')) # Or redirect to a pending requests page

    # Create the join request
    join_request = GroupJoinRequest(
        group=group,
        user=current_user,
        status='pending'
    )
    db.session.add(join_request)
    db.session.commit()

    flash('Your request to join has been sent to the group administrators.', 'success')
    return redirect(url_for('forum.index'))

@bp.route('/group/<int:group_id>/manage_requests')
@login_required
def manage_join_requests(group_id):
    """Displays and manages join requests for a group (admin only)."""
    group = Group.query.get_or_404(group_id)

    # Check if current user is an admin of this group
    if group.created_by != current_user:
        flash('You do not have permission to manage join requests for this group.', 'danger')
        return redirect(url_for('forum.view_group', group_id=group.id))

    pending_requests = GroupJoinRequest.query.filter_by(
        group_id=group.id,
        status='pending'
    ).all()

    return render_template('forum/manage_join_requests.html',
                           group=group,
                           pending_requests=pending_requests)

@bp.route('/request/<int:request_id>/accept', methods=['POST'])
@login_required
def accept_join_request(request_id):
    """Accepts a group join request (group admin only)."""
    join_request = GroupJoinRequest.query.get_or_404(request_id)
    group = join_request.group

    # Check if current user is an admin of this group
    if group.created_by != current_user:
        flash('You do not have permission to manage this join request.', 'danger')
        return redirect(url_for('forum.view_group', group_id=group.id))

    # Check if request is still pending
    if join_request.status != 'pending':
        flash('This request is no longer pending.', 'warning')
        return redirect(url_for('forum.manage_join_requests', group_id=group.id))

    # Add the user to the group members
    if join_request.user not in group.members:
        group.members.append(join_request.user)

    # Update the request status
    join_request.status = 'accepted'
    db.session.commit()

    flash(f'Request from {join_request.user.first_name} accepted.', 'success')
    return redirect(url_for('forum.manage_join_requests', group_id=group.id))

@bp.route('/request/<int:request_id>/reject', methods=['POST'])
@login_required
def reject_join_request(request_id):
    """Rejects a group join request (group admin only)."""
    join_request = GroupJoinRequest.query.get_or_404(request_id)
    group = join_request.group
    
    # Check if current user is an admin of this group
    if group.created_by != current_user:
        flash('You do not have permission to manage this join request.', 'danger')
        return redirect(url_for('forum.view_group', group_id=group.id))

    # Check if request is still pending
    if join_request.status != 'pending':
        flash('This request is no longer pending.', 'warning')
        return redirect(url_for('forum.manage_join_requests', group_id=group.id))

    # Update the request status
    join_request.status = 'rejected'
    db.session.commit()

    flash(f'Request from {join_request.user.first_name} rejected.', 'info')
    return redirect(url_for('forum.manage_join_requests', group_id=group.id))

@bp.route('/group/<int:group_id>/leave', methods=['POST'])
@login_required
def leave_group(group_id):
    """Allows a user to leave a group."""
    group = Group.query.get_or_404(group_id)
    
    # Verifica se l'utente è un membro del gruppo
    if group not in current_user.groups:
        flash('You are not a member of this group.', 'warning')
        return redirect(url_for('forum.index'))
    
    # Verifica se è l'ultimo admin prima di permettere di lasciare il gruppo
    # Temporaneamente, controlliamo se è il creatore e l'unico membro.
    # Questa logica potrebbe richiedere una revisione più approfondita se i ruoli admin sono più complessi.
    is_creator = (group.created_by == current_user)
    is_only_member = (len(group.members) == 1)
    
    if is_creator and is_only_member:
         flash('As the creator and only member, you cannot leave the group.', 'danger')
         return redirect(url_for('forum.view_group', group_id=group.id))

    # Rimuovi l'utente dalla relazione group.members
    group.members.remove(current_user)
    db.session.commit()
    
    flash('You have left the group.', 'success')
    return redirect(url_for('forum.index')) 