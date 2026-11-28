import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q

MAX_CAPACITY = 2**31 - 1
MAX_PRICE_CENTS = 2**53 - 1


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        CANCELLED = 'cancelled', 'Cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='events'
    )
    name = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    capacity = models.IntegerField()
    price_cents = models.BigIntegerField()
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(capacity__gte=1, capacity__lte=MAX_CAPACITY),
                name='coredata_event_capacity_range',
            ),
            models.CheckConstraint(
                condition=Q(price_cents__gte=1, price_cents__lte=MAX_PRICE_CENTS),
                name='coredata_event_price_range',
            ),
            models.CheckConstraint(
                condition=Q(status__in=['draft', 'published', 'cancelled']),
                name='coredata_event_status_valid',
            ),
        ]
        indexes = [
            models.Index(fields=['owner', 'id'], name='cd_event_owner_id_idx'),
            models.Index(fields=['status', 'starts_at'], name='cd_event_status_start_idx'),
        ]


class Ticket(models.Model):
    class Channel(models.TextChoices):
        WEB = 'web', 'Web'
        PARTNER = 'partner', 'Partner'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        DECLINED = 'declined', 'Declined'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='tickets')
    code = models.CharField(max_length=12, unique=True)
    channel = models.CharField(max_length=7, choices=Channel.choices)
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='tickets',
        null=True,
        blank=True,
    )
    buyer_email = models.EmailField(max_length=254, db_collation='C')
    price_cents = models.BigIntegerField()
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.PENDING)
    checked_in_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(code__regex=r'^[A-Z0-9]{12}$'),
                name='coredata_ticket_code_format',
            ),
            models.CheckConstraint(
                condition=Q(channel__in=['web', 'partner']),
                name='coredata_ticket_channel_valid',
            ),
            models.CheckConstraint(
                condition=Q(
                    status__in=[
                        'pending',
                        'confirmed',
                        'declined',
                        'cancelled',
                        'refunded',
                    ]
                ),
                name='coredata_ticket_status_valid',
            ),
            models.CheckConstraint(
                condition=Q(price_cents__gte=1, price_cents__lte=MAX_PRICE_CENTS),
                name='coredata_ticket_price_range',
            ),
            models.CheckConstraint(
                condition=(Q(channel='web', participant__isnull=False))
                | Q(channel='partner', participant__isnull=True),
                name='coredata_ticket_buyer_xor',
            ),
        ]
        indexes = [
            models.Index(fields=['event', 'status'], name='cd_ticket_event_status_idx'),
            models.Index(fields=['participant', 'created_at'], name='cd_ticket_part_created_idx'),
        ]


class PaymentJob(models.Model):
    class Outcome(models.TextChoices):
        APPROVED = 'approved', 'Approved'
        DECLINED = 'declined', 'Declined'

    class State(models.TextChoices):
        QUEUED = 'queued', 'Queued'
        DONE = 'done', 'Done'
        IGNORED = 'ignored', 'Ignored'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.OneToOneField(Ticket, on_delete=models.PROTECT, related_name='payment_job')
    outcome = models.CharField(max_length=8, choices=Outcome.choices)
    due_at = models.DateTimeField()
    state = models.CharField(max_length=7, choices=State.choices, default=State.QUEUED)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(outcome__in=['approved', 'declined']),
                name='coredata_payment_job_outcome_valid',
            ),
            models.CheckConstraint(
                condition=Q(state__in=['queued', 'done', 'ignored']),
                name='coredata_payment_job_state_valid',
            ),
            models.CheckConstraint(
                condition=(Q(state='queued', processed_at__isnull=True))
                | (Q(state__in=['done', 'ignored']) & Q(processed_at__isnull=False)),
                name='coredata_payment_job_state_processed',
            ),
        ]
        indexes = [
            models.Index(
                fields=['due_at'],
                condition=Q(state='queued'),
                name='cd_job_queued_due_idx',
            )
        ]


class WorkerHeartbeat(models.Model):
    worker_id = models.CharField(primary_key=True, max_length=100)
    last_seen = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(auto_now_add=True)
