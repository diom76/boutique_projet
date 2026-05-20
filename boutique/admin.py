from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .models import Produit, Commande


#---Titre de l'interface admin---

admin.site.site_header = "Administration Boutique"
admin .site.site_title = "Boutique Admin"
admin.site.index_title = "Tableau de bord"

#----Afficher les commandes dans un produit-----

class CommandeInline(admin.TabularInline):
    model = Commande
    extra = 0
    fields =('client_nom', 'client_email', 'quantite', 'statut')
    
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display =('nom', 'prix', 'stock', 'disponible',  'date_ajout')
    list_filter = ('disponible',)
    search_fields = ('nom', 'description')
    list_editable = ('disponible',)
    ordering = ('nom',)
    inlines = [CommandeInline]
    
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('produit', 'client_nom', 'quantite', 'afficher_statut', 'total', 'date_commande')
    list_filter = ('statut','date_commande')
    search_fields = ('client_nom', 'client_email')
    date_hierarchy = 'date_commande'
    actions = ['annuler_commandes']
        
    
    @admin.display(description='Statut')
    def afficher_statut(self,obj):
        return obj.get_statut_display()
    
    @admin.display(description='Total')
    def total(self, obj):
      montant = obj.produit.prix * obj.quantite
      return format_html('<b>{} € </b>',montant)

# Action : annuler les commandes sélectionnées
    @admin.action(description='Annuler les commandes sélectionnées')
    def annuler_commandes(self, request, queryset):
       nb = queryset.update(statut='ANNULEE')
       self.message_user(
        request,
        f'{nb}commnade(s) annulée(s).',
        messages.WARNING
      )        
    
