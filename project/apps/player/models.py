from django.contrib.auth.models import AbstractUser
from utils.base import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Player(AbstractUser):
    pass

class PlayerData(BaseModel):
    player = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        related_name="data",
        verbose_name=_("player"),
    )
    position = models.JSONField(default=[[-1969.4, 137.85, 27.69]], blank=True, null=True)
    rotation = models.FloatField(default=0, blank=True, null=True)
    skin = models.IntegerField(default=0, blank=True, null=True)
    interior = models.IntegerField(default=0, blank=True, null=True)
    dimension = models.IntegerField(default=0, blank=True, null=True)
    team = models.CharField(default=0, max_length=50, blank=True, null=True)
    health = models.IntegerField(default=100, blank=True, null=True)
    money = models.IntegerField(default=0, blank=True, null=True)
    weapons = models.JSONField(default=[[]], blank=True, null=True)
    armor = models.FloatField(default=100.00, blank=True, null=True)
    clothes = models.JSONField(default=[[["vestblack", "vest", 0], ["player_face", "head", 1], ["jeansdenim", "jeans", 2], ["sneakerbincblk", "sneaker", 3]]], blank=True, null=True)
    wantedlevel = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'tb_player_data'