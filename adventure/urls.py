from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
<<<<<<< HEAD
    url('rooms' api.rooms),
]
=======
    url('get_rooms', api.get_rooms)
]
>>>>>>> 7be7b55d4d8f0c45c57b305c3a836732324c0147
