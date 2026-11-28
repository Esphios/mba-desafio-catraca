import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Q
from django.utils import timezone

from accounts.email_policy import CanonicalEmailField, normalize_email


class UserQuerySet(models.QuerySet):
    _allow_canonical_email_expression = False

    def _clone(self):
        clone = super()._clone()
        clone._allow_canonical_email_expression = self._allow_canonical_email_expression
        return clone

    def update(self, **kwargs):
        if 'email' in kwargs and not self._allow_canonical_email_expression:
            kwargs['email'] = normalize_email(kwargs['email'])
        return super().update(**kwargs)

    def bulk_update(self, objs, fields, batch_size=None):
        fields = tuple(fields)
        if 'email' in fields:
            objs = tuple(objs)
            for user in objs:
                user.email = normalize_email(user.email)
            queryset = self._chain()
            queryset._allow_canonical_email_expression = True
            return super(UserQuerySet, queryset).bulk_update(objs, fields, batch_size)
        return super().bulk_update(objs, fields, batch_size)


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.ORGANIZER)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields['is_staff'] or not extra_fields['is_superuser']:
            raise ValueError('Superuser must have is_staff=True and is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        PARTICIPANT = 'participant', 'Participant'
        ORGANIZER = 'organizer', 'Organizer'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = CanonicalEmailField(max_length=254, unique=True, db_collation='C')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=11, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        base_manager_name = 'objects'
        constraints = [
            models.CheckConstraint(
                condition=Q(role__in=['participant', 'organizer']),
                name='accounts_user_role_valid',
            )
        ]
