from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import CommandeForm
from .models import Commande, Produit
from .forms import CommandeForm, ContactForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required
def profil(request):
    commandes = Commande.objects.filter(utilisateur=request.user).order_by('-date_commande')
    return render(request,'boutique/profil.html',{
        'commandes':commandes,
    })
    
@staff_member_required
def admin_dashboard(request):
    
    total_produits = Produit.objects.count()
    total_commandes = Commande.objects.count()
    total_utilisateurs = User.objects.count()
    
    total_ventes = sum(c.total for c in Commande.objects.all())
    
    commandes_recentes = Commande.objects.order_by('-date_commande')[:5]
    
    context = {
        'total_produits': total_produits,
        'total_commandes': total_commandes,
        'total_utilisateurs': total_utilisateurs,
        'total_ventes': total_ventes,
        'commandes_recentes': commandes_recentes,
    }
    return render(
        request,'boutique/admin_dashboard.html',
        context
    )
        
        
    
    
def liste_produits(request):
    produits = Produit.objects.filter(disponible=True)
    query = request.GET.get('q')
    
    if query:
        produits = produits.filter(nom__icontains=query)
    return render (request,'boutique/liste.html',{
        'produits':produits,
        'query':query,
    })    

def detail_produit(request,pk):
    produit = get_object_or_404(Produit,pk=pk)
    form = CommandeForm()
    
    if request.method =='POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande =form.save(commit=False)
            commande.produit = produit
            commande.save()
            
            #Verifier que le stock est suffisant
            if commande.quantite > produit.stock:
                messages.error(request,f'Stock insuffisant ! Il reste seulement {produit.stock} article(s).')
                return render (request,'boutique/detail.html',{
                    'produit':produit,
                    'form':form,
                })    
            commande.save()
            
            #Diminuer le stock
            produit.stock -= commande.quantite
            produit.save()
            return redirect('boutique:confirmation',pk=commande.pk)
    return render(request,'boutique/detail.html',{
        'produit':produit,
        'form' :form,
    })    
    
    
def confirmation(request,pk):
    from.models import Commande
    commande = get_object_or_404(Commande,pk=pk)
    total = commande.produit.prix*commande.quantite
    return render(request,'boutique/confirmation.html',{
        'commande':commande,
        'total':total,
    })    

def contact(request):
    if request.method == 'POST':
        form =ContactForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            messages.success(request, f'Merci {nom} ! Votre message a été envoyé.')
            return redirect('boutique:contact')
    form = ContactForm()
    return render(request, 'boutique/contact.html',{'form':form})    

def inscription(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, f'Bienvenue {user.username} !')
            return redirect('boutique:liste')
        return render(request,'registration/inscription.html', {'form':form})
    form = UserCreationForm()
    return render(request,'registration/inscription.html',{'form':form})    