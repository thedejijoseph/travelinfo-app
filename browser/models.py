from django.db import models


class State(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Terminal(models.Model):
    name = models.CharField(max_length=300)
    AIR = "air"
    ROAD = "road"
    RAIL = "rail"
    SUPPORTED_MODES = (
        (AIR, 'Air'),
        (ROAD, 'Road'),
        (RAIL, 'Rail')
    )
    mode = models.CharField(max_length=12, choices=SUPPORTED_MODES)
    state = models.ForeignKey('State', on_delete=models.PROTECT)
    # set to protect cause states should not be deleted easily
    description = models.TextField()
    dest_terminals = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f"{self.name} - {self.state}"
