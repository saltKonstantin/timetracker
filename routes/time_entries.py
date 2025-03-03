from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from models import db, TimeEntry
from forms import TimeEntryForm, QuickEntryForm

entries_bp = Blueprint('entries', __name__)

@entries_bp.route('/')
@login_required
def index():
    # Redirect to timeline view as the main dashboard
    return redirect(url_for('entries.timeline'))

@entries_bp.route('/dashboard')
@login_required
def dashboard():
    # Default to today's date
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        selected_date = datetime.now()
    
    # Get start and end of day
    start_of_day = datetime.combine(selected_date.date(), datetime.min.time())
    end_of_day = datetime.combine(selected_date.date(), datetime.max.time())
    
    # Get entries for the selected day
    entries = TimeEntry.query.filter_by(user_id=current_user.id).filter(
        TimeEntry.start_time >= start_of_day,
        TimeEntry.start_time <= end_of_day
    ).order_by(TimeEntry.start_time).all()
    
    # Create forms
    entry_form = TimeEntryForm()
    quick_form = QuickEntryForm()
    
    # Default form values to selected date at current time
    if not request.method == 'POST':
        now = datetime.now()
        entry_form.start_time.data = now
        entry_form.end_time.data = now + timedelta(minutes=15)
    
    return render_template(
        'time_entries/dashboard.html',
        title='Time Tracker',
        entries=entries,
        selected_date=selected_date,
        entry_form=entry_form,
        quick_form=quick_form,
        timedelta=timedelta
    )

@entries_bp.route('/timeline')
@login_required
def timeline():
    # Default to today's date
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        selected_date = datetime.now()
    
    # Calculate the Monday of the current week (regardless of the current day)
    weekday = selected_date.weekday()  # Monday is 0, Sunday is 6
    # Subtract the current weekday to get to Monday
    week_start = selected_date - timedelta(days=weekday)
    
    # Calculate the Sunday of the current week
    week_end = week_start + timedelta(days=6)
    
    # Generate list of weekdays (always Monday through Sunday)
    weekdays = [week_start + timedelta(days=i) for i in range(7)]
    
    # Get entries for the entire week
    start_of_week = datetime.combine(week_start.date(), datetime.min.time())
    end_of_week = datetime.combine(week_end.date(), datetime.max.time())
    
    all_entries = TimeEntry.query.filter_by(user_id=current_user.id).filter(
        TimeEntry.start_time >= start_of_week,
        TimeEntry.start_time <= end_of_week
    ).order_by(TimeEntry.start_time).all()
    
    # Create forms
    entry_form = TimeEntryForm()
    quick_form = QuickEntryForm()
    
    # Default form values to selected date at current time
    if not request.method == 'POST':
        now = datetime.now()
        entry_form.start_time.data = now
        entry_form.end_time.data = now + timedelta(minutes=15)
    
    today = datetime.now()
    
    return render_template(
        'time_entries/timeline.html',
        title='Time Tracker - Weekly Timeline',
        entries=all_entries,
        all_entries=all_entries,
        selected_date=selected_date,
        week_start=week_start,
        week_end=week_end,
        weekdays=weekdays,
        today=today,
        entry_form=entry_form,
        quick_form=quick_form,
        timedelta=timedelta
    )

@entries_bp.route('/entry/new', methods=['POST'])
@login_required
def create_entry():
    form = TimeEntryForm()
    if form.validate_on_submit():
        entry = TimeEntry(
            user_id=current_user.id,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(entry)
        db.session.commit()
        flash('Time entry added!')
        
        # Redirect to timeline view
        return redirect(url_for('entries.timeline', date=form.start_time.data.strftime('%Y-%m-%d')))
    
    # If validation fails, flash errors and return to timeline
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", "error")
    
    return redirect(url_for('entries.timeline'))

@entries_bp.route('/entry/update', methods=['POST'])
@login_required
def update_entry_ajax():
    data = request.json
    entry_id = data.get('id')
    new_start = data.get('start_time')
    new_end = data.get('end_time')
    
    entry = TimeEntry.query.get_or_404(entry_id)
    
    # Security check - only owner can update
    if entry.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You cannot edit this entry.'}), 403
    
    try:
        entry.start_time = datetime.fromisoformat(new_start)
        entry.end_time = datetime.fromisoformat(new_end)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@entries_bp.route('/entry/quick', methods=['POST'])
@login_required
def quick_entry():
    form = QuickEntryForm()
    if form.validate_on_submit():
        try:
            # Parse duration (expecting format like "1.5" for 1.5 hours)
            duration_hours = float(form.duration.data)
            duration_minutes = int(duration_hours * 60)
            
            # Create entry starting now
            start_time = datetime.now()
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            entry = TimeEntry(
                user_id=current_user.id,
                description=form.description.data,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(entry)
            db.session.commit()
            flash('Time entry added!')
        except ValueError:
            flash('Invalid duration format. Please use a number like 0.25 for 15 minutes or 1.5 for 1.5 hours.')
    
    # Redirect to timeline instead of dashboard
    return redirect(url_for('entries.timeline'))

@entries_bp.route('/entry/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = TimeEntry.query.get_or_404(entry_id)
    
    # Security check - only owner can edit
    if entry.user_id != current_user.id:
        flash('You cannot edit this entry.')
        return redirect(url_for('entries.timeline'))
    
    form = TimeEntryForm()
    
    if request.method == 'GET':
        form.description.data = entry.description
        form.start_time.data = entry.start_time
        form.end_time.data = entry.end_time
        return render_template('time_entries/entry_form.html', form=form, entry=entry)
    
    if form.validate_on_submit():
        entry.description = form.description.data
        entry.start_time = form.start_time.data
        entry.end_time = form.end_time.data
        db.session.commit()
        flash('Entry updated!')
        # Redirect to timeline view
        return redirect(url_for('entries.timeline', date=entry.start_time.strftime('%Y-%m-%d')))
    
    return render_template('time_entries/entry_form.html', form=form, entry=entry)

@entries_bp.route('/entry/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = TimeEntry.query.get_or_404(entry_id)
    
    # Security check - only owner can delete
    if entry.user_id != current_user.id:
        flash('You cannot delete this entry.')
        return redirect(url_for('entries.timeline'))
    
    date_str = entry.start_time.strftime('%Y-%m-%d')
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted!')
    
    # Redirect to timeline view
    return redirect(url_for('entries.timeline', date=date_str))