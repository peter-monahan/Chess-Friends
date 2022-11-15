from flask.cli import AppGroup
from .users import seed_users, undo_users
from .friend_requests import seed_friend_requests, undo_friend_requests
from .friends import seed_friends, undo_friends
from .dm_views import seed_dms, undo_dms
from .messages import seed_messages, undo_messages
# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
  seed_users()
  seed_friend_requests()
  seed_friends()
  seed_dms()
  seed_messages()
  # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
  undo_users()
  undo_friend_requests()
  undo_friends()
  undo_dms()
  undo_messages()
  # Add other undo functions here


@seed_commands.command('users')
def seed_just_users():
  seed_users()


@seed_commands.command('undo users')
def undo_just_users():
  undo_users()


@seed_commands.command('friend_requests')
def seed_just_friend_requests():
  seed_friend_requests()


@seed_commands.command('undo friend_requests')
def undo_just_friend_requests():
  undo_friend_requests()



@seed_commands.command('friends')
def seed_just_friends():
  seed_friends()


@seed_commands.command('undo friends')
def undo_just_friends():
  undo_friends()



@seed_commands.command('dm_views')
def seed_just_dms():
  seed_dms()


@seed_commands.command('undo dm_views')
def undo_just_dms():
  undo_dms()



@seed_commands.command('messages')
def seed_just_messages():
  seed_messages()


@seed_commands.command('undo messages')
def undo_just_messages():
  undo_messages()
