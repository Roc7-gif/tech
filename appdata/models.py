from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class FormationStatus(models.TextChoices):
    EN_COURS = 'EN_COURS', 'En cours'
    TERMINEE = 'TERMINEE', 'Terminée'
    BIENTOT = 'BIENTÔT', 'Bientôt'  



class Userinfo(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ######     Parties Project        #######

class Project_Categ(models.Model): 
    Title = models.CharField(max_length=300)
    def __str__(self) -> str:
        return self.Title
class Technologies(models.Model): 
    Title = models.CharField(max_length=300)
    def __str__(self) -> str:
        return self.Title

class Projects(models.Model): 
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='images', null=False)
    category = models.ForeignKey(Project_Categ , on_delete=models.CASCADE)
    created_at= models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.title
class Tech_Project(models.Model): 
    Technologies = models.ForeignKey(Technologies , on_delete=models.CASCADE)
    Project = models.ForeignKey(Projects , on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.Technologies.Title

class Formations(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='images', null=False)
    statut = models.CharField(
        max_length=20,
        choices=FormationStatus.choices,
        default=FormationStatus.BIENTOT)
    categorie = models.ForeignKey(Project_Categ, on_delete=models.CASCADE,null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    price = models.PositiveIntegerField(null=True)
    place  = models.CharField(max_length=200,null=True)
    heure  = models.CharField(max_length=200,null=True)


class Participation (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    formation = models.ForeignKey(Formations , on_delete=models.CASCADE)
    paye = models.BooleanField(default=False)
    attestation  = models.FileField(upload_to='attestation',null=True)
    class Meta:
        unique_together = ('user', 'formation')  # ← Empêche les doublons
