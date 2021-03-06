from django.db import models
from django.db import transaction
from django.contrib.auth.models import User
# Create your models here.

#solo para descuentos
class Descuento(models.Model):
    param = models.CharField(max_length=50, primary_key=True)
    value = models.IntegerField(null=True)
    def __unicode__(self):
        return self.param

    class Meta:
        db_table = 'descuentos'


class UserJava(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=200)
    #nivel de permisos
    CHOICES = [ (0 , 'vendedor/cajero'),
                (1 , 'supervisor'),
                (2 , 'administrador'),
                (3 , 'super')]
    nivel = models.IntegerField(choices=CHOICES)
    is_staff = models.BooleanField() #si es staff => tiene una cuenta de
                                     #django
    last_factura = models.IntegerField()
    def __unicode__(self):
        return self.username
    class Meta:
        db_table = 'usuarios'

@transaction.commit_on_success
def createUser(username, password, nivel):
#createUser given the username, password, nivel
    is_staff = nivel > 0
    #Create user for java client
    usuario = UserJava()
    usuario.username = username
    usuario.password = generatePass(password)
    usuario.nivel = nivel
    usuario.last_factura = 0
    usuario.is_staff = is_staff
    usuario.save()
    if is_staff:
        User.objects.create_user(username,
                                'test@test.test',
                                password)

def generatePass(password):
    import hashlib
    m = hashlib.sha1()
    m.update(password)
    return m.hexdigest()

def getUserJava(username):
    return UserJava.objects.get(username=username)
