from django.db import models
from django.contrib.auth.models import User


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    image  =models.ImageField(
        upload_to='produits/',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return self.nom
    
class Commande(models.Model):
    STATUS = [
        ('EN_ATTENTE', 'En attente'),
        ('CONFIRMEE','Confirmée'),
        ('LIVREE','Livrée'),
        ('ANNULEE', 'Annulée'),
    ]    
    
    produit = models.ForeignKey(
              Produit,
              on_delete=models.CASCADE,
              related_name='commandes'
           )
    utilisateur =models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client_nom = models.CharField(max_length=100)
    client_email =models.EmailField()
    quantite = models.PositiveIntegerField(default=0)
    date_commande = models.DateTimeField(auto_now_add=True)
    
    statut  = models.CharField(
        max_length=20,
        choices= STATUS,
        default='EN_ATTENTE'
        )
    def __str__(self):
        return f"Commande de {self.client_nom} - {self.produit.nom}" 
    
    @property
    def total(self):
        return self.produit.prix * self.quantite