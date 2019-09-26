from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

class Room(models.Model):  # mod this
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y

    def __str__(self):
        s_to = self.s_to
        if s_to:
            s_to = self.s_to.id
        e_to = self.e_to
        if e_to:
            e_to = self.e_to.id
        w_to = self.w_to
        if w_to:
            w_to = self.w_to.id
        n_to = self.n_to
        if n_to:
            n_to = self.n_to.id


        return f"name:{self.name}, description:{self.description}, id:{self.id}, s_to:{s_to}, e_to:{e_to}, w_to:{w_to}, n_to:{n_to},  x:{self.x}, y:{self.y}"

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


    # title = models.CharField(max_length=50, default="DEFAULT TITLE")
    # description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    # n_to = models.IntegerField(default=0)
    # s_to = models.IntegerField(default=0)
    # e_to = models.IntegerField(default=0)
    # w_to = models.IntegerField(default=0)
    # x = models.IntegerField(default=0)
    # y = models.IntegerField(default=0)
    # def connectRooms(self, destinationRoom, direction):
    #     destinationRoomID = destinationRoom.id
    #     try:
    #         destinationRoom = Room.objects.get(id=destinationRoomID)
    #     except Room.DoesNotExist:
    #         print("That room does not exist")
    #     else:
    #         if direction == "n":
    #             self.n_to = destinationRoomID
    #         elif direction == "s":
    #             self.s_to = destinationRoomID
    #         elif direction == "e":
    #             self.e_to = destinationRoomID
    #         elif direction == "w":
    #             self.w_to = destinationRoomID
    #         else:
    #             print("Invalid direction")
    #             return
    #         self.save()
    # def playerNames(self, currentPlayerID):
    #     return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    # def playerUUIDs(self, currentPlayerID):
    #     return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()