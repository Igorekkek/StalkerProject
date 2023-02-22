from django.db import models

class Swan(models.Model):
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    idd = models.IntegerField()
    int0 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'<id = {self.idd} | int0 = {self.int0} | (x, y) = ({self.x, self.y}>'
    
class Detector(models.Model):
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    idd = models.IntegerField()
    swans = models.ManyToManyField(Swan, blank=True)

    def __str__(self):
        return f'<idd = {self.idd} | (x, y) = ({self.x, self.y})>'
