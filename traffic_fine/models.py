from __future__ import unicode_literals

from django.db import models

def upload_to_traffic_fine_city(instance, filename):
    path = "traffic_fine/city/"
    ext = filename.split('.')[-1]
    name = slugify(instance.name.encode("utf-8")) + '.' + ext
    return os.path.join(path, name)

class TrafficFineCity(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True  )
    icon = models.FileField(upload_to=upload_to_traffic_fine_city)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        db_table='web_trafficfinecity'
        verbose_name = 'Traffic Fine City'
        verbose_name_plural = 'Traffic Fine Cities'
        ordering = ('order',)

    def __unicode__(self):
        return self.name

def upload_to_traffic_fine_category(instance, filename):
    path = "traffic_fine/category/"
    ext = filename.split('.')[-1]
    name = slugify(instance.name.encode("utf-8")) + '.' + ext
    return os.path.join(path, name)

class TrafficFineCategory(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True )
    icon = models.FileField(upload_to=upload_to_traffic_fine_category)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        db_table = 'web_trafficfinecategory'
        verbose_name = 'Traffic Fine Category'
        verbose_name_plural = 'Traffic Fine Categories'
        ordering = ('order',)

    def __unicode__(self):
        return self.name

class TrafficFine(models.Model):

    traffic_offense = models.CharField(max_length=255, blank=False )
    category = models.ForeignKey(TrafficFineCategory, blank=False, null=False)
    city = models.ForeignKey(TrafficFineCity, blank=True, null=True)
    simplified = models.TextField(blank=False )
    fine_first_offense = models.CharField(max_length=255, blank=False)
    jail_first_offense = models.CharField(max_length=255, blank=True )
    fine_second_offense = models.CharField(max_length=255, blank=True)
    jail_second_offense = models.CharField(max_length=255, blank=True )
    text_of_hyperlink = models.TextField(blank=True )
    hyperlink = models.TextField(blank=True )

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        db_table = 'web_trafficfine'
        unique_together = (("traffic_offense", "category", "city"),)
        verbose_name = 'Traffic Fine'
        verbose_name_plural = 'Traffic Fines'
        ordering = ('order',)

    def __unicode__(self):
        return self.traffic_offense

    def get_url(self):
        return reverse('traffic-fine', args=[slugify(self.city.name.encode("utf-8")), slugify(self.category.name.encode("utf-8")), slugify(self.traffic_offense.encode("utf-8")),])

