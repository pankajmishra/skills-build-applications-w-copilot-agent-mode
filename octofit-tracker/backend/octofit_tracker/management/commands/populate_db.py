from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        # Use Djongo's connection to drop collections directly to avoid PK issues
        from django.db import connection
        db = connection.cursor().db_conn.client['octofit_db']
        # Drop both possible collection names used by Djongo
        for col in ('octofit_tracker_activity', 'octofit_tracker_workout', 'octofit_tracker_leaderboard', 'octofit_tracker_user', 'octofit_tracker_team', 'octofit_tracker_workout_suggested_for', 'user', 'team', 'activity', 'workout', 'leaderboard'):
            try:
                db[col].drop()
            except Exception:
                pass

        # Fallback: flush database if above fails (for dev only)
        # from django.core.management import call_command
        # call_command('flush', '--noinput')

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Team Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='Team DC Superheroes')

        # Create Users
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Ensure unique index on email for both possible collection names
        for users_collection in ('user', 'octofit_tracker_user'):
            try:
                db[users_collection].create_index('email', unique=True)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not create unique index on {users_collection}.email: {e}'))

        # Create Activities
        Activity.objects.create(user=users[0], type='Running', duration=30, date='2026-01-01')
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date='2026-01-02')
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date='2026-01-03')
        Activity.objects.create(user=users[3], type='Yoga', duration=40, date='2026-01-04')

        # Create Workouts
        w1 = Workout.objects.create(name='Hero HIIT', description='High intensity interval training for heroes')
        w2 = Workout.objects.create(name='Power Yoga', description='Yoga for strength and flexibility')
        w1.suggested_for.set([users[0], users[1]])
        w2.suggested_for.set([users[2], users[3]])

        # Create Leaderboards
        Leaderboard.objects.create(team=marvel, total_points=100)
        Leaderboard.objects.create(team=dc, total_points=120)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
