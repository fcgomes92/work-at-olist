from django.db import models
from django.utils import timezone

from .util.generators import generate_uid
from . import strings


class Channel(models.Model):
    uid = models.CharField(verbose_name=strings.CHANNEL_FIELD_UID, max_length=512, unique=True)
    name = models.CharField(verbose_name=strings.CHANNEL_FIELD_NAME, max_length=128, unique=True)
    description = models.TextField(verbose_name=strings.CHANNEL_FIELD_DESCRIPTION, blank=True, default='')

    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        app_label = strings.APP_LABEL
        verbose_name = strings.CHANNEL_MODEL_VERBOSE
        verbose_name_plural = strings.CHANNEL_MODEL_VERBOSE_PLURAL
        ordering = ['-updated', '-created', ]

    def __str__(self):
        return ''

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.uid = generate_uid(**dict(name=self.name, id=self.id))
        self.updated = timezone.now()
        super(Channel, self).save(*args, **kwargs)


class Category(models.Model):
    uid = models.CharField(verbose_name=strings.CATEGORY_FIELD_UID, max_length=512, unique=True)
    channel = models.ForeignKey('Channel', related_name='categories')
    name = models.CharField(verbose_name=strings.CATEGORY_FIELD_NAME, max_length=128)
    parent = models.ForeignKey('Category', related_name='children', null=True, default=None)
    description = models.TextField(verbose_name=strings.CATEGORY_FIELD_DESCRIPTION, blank=True, default='')

    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        app_label = strings.APP_LABEL
        verbose_name = strings.CATEGORY_MODEL_VERBOSE
        verbose_name_plural = strings.CATEGORY_MODEL_VERBOSE_PLURAL
        ordering = ['-updated', '-created', ]
        unique_together = ('channel', 'name', 'parent')

    def __str__(self):
        if self.parent:
            return '{} > {}'.format(self.parent, self.name)
        else:
            return self.name

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.uid = generate_uid(**dict(name=self.name, id=self.id))
        self.updated = timezone.now()
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    uid = models.CharField(verbose_name=strings.PRODUCT_FIELD_UID, max_length=512, unique=True)
    channel = models.ForeignKey('Channel', related_name='channel_products', null=True, default=None)
    category = models.ForeignKey('Category', related_name='products', null=True, default=None)
    name = models.CharField(verbose_name=strings.PRODUCT_FIELD_NAME, max_length=128)
    description = models.TextField(verbose_name=strings.PRODUCT_FIELD_DESCRIPTION, blank=True, default='')

    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        app_label = strings.APP_LABEL
        verbose_name = strings.PRODUCT_MODEL_VERBOSE
        verbose_name_plural = strings.PRODUCT_MODEL_VERBOSE_PLURAL
        ordering = ['-updated', '-created', ]

    def __str__(self):
        return ''

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.uid = generate_uid(**dict(name=self.name, id=self.id))
        self.updated = timezone.now()
        super(Product, self).save(*args, **kwargs)
