USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLE_CHOICES = (
    (USER, 'user'),
    (ADMIN, 'admin'),
    (MODERATOR, 'moderator'),
)

STANDARD_FIELD_LENGTH = 150
EMAIL_FIELD_LENGTH = 254
MAX_ROLE_LENGTH = max([len(role) for role, _ in ROLE_CHOICES])
