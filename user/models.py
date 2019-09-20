import hashlib

from django.utils import timezone
from django.db import models, transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
	"""Define a model manager for User model with no username field."""

	use_in_migrations = True

	def password_encrypt(password):
		salt = None
		return hashlib.sha256(salt.encode() + password.encode()).hexdigest()

	def _create_user(self, email, password, **extra_fields):
		sid = transaction.savepoint()

		try:
			"""Create and save a User with the given email and password."""
			if not email:
				raise ValueError('The given email must be set')
			email = self.normalize_email(email)
			user = self.model(email=email, **extra_fields)
			user.set_password(password)
			user.save(using=self._db)

			transaction.savepoint_commit(sid)

			return user
		except IntegrityError as e:
			transaction.savepoint_rollback(sid)
			print(e.message)
			
			return False

	def create_user(self, email, password=None, **extra_fields):
		"""Create and save a regular User with the given email and password."""
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		"""Create and save a SuperUser with the given email and password."""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)

	# get all users
	def all_user(self):
		return self.filter(is_active=True)

	def get_user(self, id):
		try:
			return self.get(id=id, is_active=True)
		except ObjectDoesNotExist:
			return False

	def update_user(self, id, data):
		sid = transaction.savepoint()

		try:
			user = self.get(id=id)
			user.first_name = data['first_name'] 
			user.last_name = data['last_name'] 
			user.email = self.normalize_email(data['email'])
			if data['password']:
				user.set_password(data['password'])
			user.save()

			transaction.savepoint_commit(sid)
		except IntegrityError as e:
			transaction.savepoint_rollback(sid)
			print(e.message)

	def delete_user(self, id):
		try:
			user = self.get(id=id)
			user.delete()
		except ObjectDoesNotExist:
			return False


class DocumentManager(models.Manager):
	def save(self, user, document_path):
		return self.create(user=user, document=document_path)


class User(AbstractUser):
	"""User model."""

	username = None
	email = models.EmailField(_('email address'), unique=True)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this site.'),
	)
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()


class Document(models.Model):
	id = models.AutoField(primary_key=True, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	document = models.CharField(max_length=100, null=True, blank=True)
	# document = models.FileField(upload_to='documents/')
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)

	objects = DocumentManager()

	def __str__(self):
		return "Document {id} is found for {user}".format(id=self.id, user=self.user)
