from django.db import models
from django.forms import model_to_dict
from django.utils import timezone


class BaseModel(models.Model):
    class Meta:
        abstract = True
    
    id = models.AutoField(primary_key=True)

    @property
    def model_name(self) -> str:
        return str(self.__class__.__name__)

    def __repr__(self) -> str:
        columns = ', '.join(f'{field}="{value}"' for field, value in model_to_dict(self).items())
        return f'{self.model_name}({columns})'


class Customer(BaseModel):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=20)
    company = models.CharField(max_length=80, default=None, blank=True, null=True)
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40, default=None, blank=True, null=True)
    country = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=10, default=None, blank=True, null=True)
    phone = models.CharField(max_length=24, default=None, blank=True, null=True)
    fax = models.CharField(max_length=24, default=None, blank=True, null=True)
    email = models.CharField(max_length=60)
    support_rep = models.ForeignKey("Employee", models.PROTECT, default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    class Meta:
        ordering = ('last_name',)


class Invoice(BaseModel):
    customer = models.ForeignKey(Customer, models.PROTECT)
    invoice_date = models.DateTimeField()
    billing_address = models.CharField(max_length=70)
    billing_city = models.CharField(max_length=40)
    billing_state = models.CharField(max_length=40, default=None, blank=True, null=True)
    billing_country = models.CharField(max_length=40)
    billing_postal_code = models.CharField(max_length=10, default=None, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class InvoiceLine(BaseModel):
    invoice = models.ForeignKey(Invoice, models.PROTECT)
    track = models.ForeignKey("Track", models.PROTECT)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()


class Playlist(BaseModel):
    play_list = models.CharField(max_length=60)

    def __str__(self):
        return self.play_list

    class Meta:
        ordering = ('play_list',)


class Employee(BaseModel):
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    title = models.CharField(max_length=20)
    reports_to = models.ForeignKey('self', default=None, blank=True, null=True, on_delete=models.CASCADE)
    birth_date = models.DateTimeField()
    hire_date = models.DateTimeField()
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=24)
    fax = models.CharField(max_length=24)
    email = models.CharField(max_length=60)

    def __str__(self):
        return '{} {}'.format(self.last_name, self.first_name)

    class Meta:
        ordering = ('last_name',)


class Artist(BaseModel):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Album(BaseModel):
    title = models.CharField(max_length=160)
    artist = models.ForeignKey(Artist, models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class MediaType(BaseModel):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Genre(BaseModel):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Track(BaseModel):
    name = models.CharField(max_length=200)
    album = models.ForeignKey(Album, models.PROTECT)
    media_type = models.ForeignKey(MediaType, models.PROTECT)
    genre = models.ForeignKey(Genre, models.PROTECT)
    composer = models.CharField(max_length=220, default=None, blank=True, null=True)
    milliseconds = models.PositiveIntegerField(default=0)
    byte_s = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class PlaylistTrack(BaseModel):
    playlist = models.ForeignKey(Playlist, models.PROTECT)
    track = models.ForeignKey(Track, models.PROTECT)

    class Meta:
        unique_together = ('playlist', 'track',)