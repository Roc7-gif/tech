from django.shortcuts import render,redirect,get_object_or_404
from .form import *
from django.views.generic import CreateView, UpdateView
from .models import Formations
from django.urls import reverse_lazy
from django.contrib.auth import *
from django.contrib import messages

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

# Create your views here.
#INSCRIPTION
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validation des champs
        errors = []
        
        if len(nom) < 2:
            errors.append("Le nom doit contenir au moins 2 caractères.")
        
        if '@' not in email:
            errors.append("Veuillez entrer une adresse email valide.")
            
        if len(message) < 10:
            errors.append("Le message doit contenir au moins 10 caractères (protection anti-spam).")
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Envoi de l'email
            try:
                send_mail(
                    f'Message de {nom}',
                    message,
                    email,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, "Votre message a été envoyé avec succès !")
                return redirect('confirmation')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'envoi : {str(e)}")
    
    return redirect('home')
def email_valide(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
def register(request):
      form=Userform()
      if request.method=='POST':
        form=Userform(request.POST)  
        password1=request.POST["password1"] 
        password2=request.POST['password2']
        if password1 != password2 : 
            message = "Mots de passe non concordants"
            return render(request,"incscription.html",{"form":form,'msg':message})

        if form.is_valid():
            Nom=request.POST["first_name"]
            Prenom=request.POST["last_name"]
            username=request.POST["username"]
            email=request.POST["email"]
            password1=request.POST["password1"]
            password2=request.POST["password2"]
                
            utilisateur=User.objects.create_user(username,email , password1,is_active=True,first_name = Nom,last_name=Prenom)
            
            messages.success(request , 'Vous êtes enregistré')
            # # subject="Bienvenue Chez Bonaco & Co"
            # message=" Bienvenue Nous somme heureux de vous compter parmis nous. Merci."
            # from_email=settings.EMAIL_HOST_USER
            # to_list=[utilisateur.email]
           
            # send_mail(subject,message,from_email,to_list,fail_silently=False)
            # current_site=get_current_site(request)
            # email_subject="Cofirmation de l'adresse"
           
            # messageConfirm=render_to_string("ecom/emailConfirm.html",{
            #    "name":username,
            #    "domain":current_site.domain,
            #    "uid":urlsafe_base64_encode(force_bytes(utilisateur.pk)),
            #    "token":Token.make_token(utilisateur)
            # })
            # email_=EmailMessage(
            # email_subject,
            # messageConfirm,
            # settings.EMAIL_HOST,
            # [utilisateur.email]
            # )
            # email_.fail_silently=False
            # email_.send()

            return redirect("login")
        else:
            message="Nom d'utilisateur existant ou mot de passe non securisé"
            return render(request,"incscription.html",{"form":form,'msg':message})
      print(form)
      return render(request,"incscription.html",{"form":form})
def connexion(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        # Authentification unique optimisée
        user = authenticate(request, username=email, password=password) or \
               authenticate(request, email=email, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(request.GET.get('next', 'home'))
            messages.error(request, "Compte non activé . Verifier votre mail de confirmation")
        else:
            messages.error(request, "Utilisateur ou mot de passe invalide")
    
    return render(request, "connect.html")
def deconnect(request):
    logout(request)
    return redirect('home')
def home(request): 
    return render(request, 'dirichlet.html')
def create_tech(request) : 
    form = TechnologiesForm()
    if request.method == 'POST':
        if form.is_valid(): 
            form.save()
            redirect('create_tech')
    return render(request, 'categ_create.html',{'form': form})

def create_categ(request) : 
    form= Project_Categform()
    if request.method=='POST':
        form  = Project_Categform(request.POST)
        if form.is_valid(): 
            form.save()
            return  redirect('admin_dashbord')
    return render(request, 'categ_create.html',{'form': form})

def contact(request): 
    return render(request, 'contact.html')
def myproject(request):
     projects =Projects.objects.all()
     data = []
     for project in projects : 
        tech = Tech_Project.objects.filter(Project = project)
        data.append(  {
           'project': project,
             'technology': tech 
        })
     filter = Project_Categ.objects.all()

     print(data)
     return render (request, 'projets.html', {'data':data,'filter':filter})

def myformation(request):
     formations = Formations.objects.all()
     return render (request, 'formations.html' ,{'formations': formations})
def create_formation(request):
    if request.method == 'POST':
        print(request.POST)
        form = FormationForm(request.POST, request.FILES)
        if form.is_valid():
            formation = form.save()
            # return redirect('formation_detatil', pk=formation.pk)
            return redirect('admin_dashbord')
        else : 
            print(form.cleaned_data )
    else:
        form = FormationForm()
    
    return render(request, 'admin.html', {'form': form})


# def update_formation(request, pk):
#     formation = get_object_or_404(Formations, pk=pk)
#     if request.method == 'POST':
#         form = FormationForm(request.POST, request.FILES, instance=formation)
#         if form.is_valid():
#             formation = form.save()
#             return redirect('formation_detail', pk=formation.pk)
#     else:
#         form = FormationForm(instance=formation)
    
#     return render(request, 'admin.html', {'form': form})


def detatilform(request,id): 
    formation = Formations.objects.get(id =id)
    inscrit = True
    details= Formations.objects.filter(categorie = formation.categorie)
    try : 
        Participation.objects.get(user = request.user, formation  = formation)

    except: 
        inscrit=False   
    return render (request , 'detailform.html',{'formation':formation,'details': details[:4], 'inscrit': inscrit})
#Projet ----------------



def createproject(request): 
    form = ProjectsForm()
    tech = Technologies.objects.all()


    if request.method == 'POST' and  request.POST.getlist('categories'): 
        techns =   request.POST.getlist('categories')
        
        form = ProjectsForm(request.POST, request.FILES)
        if form.is_valid() :
            project= form.save()
            for i in techns: 
                Technologie = Technologies.objects.get(id = i)
                Tech_Project.objects.create(Project= project , Technologies=Technologie   )
            return redirect('myproject')
    return render(request,'create_projet.html',{'form': form,'tech': tech})
    
def projectdetail (request,id):
    projet = Projects.objects.get(id =id)
    filter = Project_Categ.objects.all()
    tech= Tech_Project.objects.filter(Project= projet )
    relation = Projects.objects.filter(category = projet.category)
    print(filter)
    return render(request,'detail_projet.html', {'projet':projet, 'technologie': tech,'details':relation ,'filter':filter})
def Formationinf(request,id) : 
    form = Formations.objects.get(id=id)
    
    try: 
        user = User.objects.get(username =  request.user )
    except : 
        return redirect('login')
 
    part = ''
   
# Créer la participation uniquement si elle n’existe pas déjà
    participation, created = Participation.objects.get_or_create(
    user=user,
    formation=form,
    defaults={'paye': False}  )

    return render(request, 'fromationinfo.html',{'participation': participation, 'formation' : form})
@login_required
def Attestation (request,id) : 
    if request.method =='POST':
        formation = Formations.objects.get(id = id)
        file  =request.FILES['file']
    for i  in  Participation.objects.filter(formation = formation): 
        i.attestation = file
        i.save() 
    return render(request, 'adminisration.html' )

#XXXXXXXXXXXXXX
@login_required
def admin_dashboard(request):
    participations = Participation.objects.select_related('user', 'formation').all()
    formations = Formations.objects.all()
    utilisateurs = User.objects.all()
    projets = Projects.objects.all()

    return render(request, 'administration.html', {
        'participations': participations,
        'formations': formations,
        'utilisateurs': utilisateurs,
        'projets': projets
    })


@login_required
def delete_participation(request, id):
    participation = get_object_or_404(Participation, id=id)
    participation.delete()
    messages.success(request, "Participation supprimée avec succès.")
    return redirect('gestion_utilisateurs')


@login_required
def gestion_utilisateurs(request):
    utilisateurs = User.objects.all()
    participations = Participation.objects.select_related('formation', 'user').all()
    return render(request, 'gestion_utilisateurs.html', {
        'utilisateurs': utilisateurs,
        'participations': participations
    })
# CRUD pour Technologies
@login_required
def list_tech(request):
    techs = Technologies.objects.all()
    return render(request, 'list_tech.html', {'categories': techs})

@login_required
def delete_tech(request, id):
    tech = get_object_or_404(Technologies, id=id)
    if request.method == 'POST':
        tech.delete()
        messages.success(request, "Technologie supprimée avec succès")
        return redirect('list_tech')
    return render(request, 'confirm_delete.html', {'object': tech})

# CRUD pour Project_Categ
@login_required
def list_categories(request):
    categories = Project_Categ.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})

@login_required
def delete_category(request, id):
    category = get_object_or_404(Project_Categ, id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Catégorie supprimée avec succès")
        return redirect('list_categories')
    return render(request, 'confirm_delete.html', {'object': category})

# CRUD pour Projects
@login_required
def list_projects(request):
    projects = Projects.objects.all()
    return render(request, 'list_projects.html', {'projects': projects})

@login_required
def delete_project(request, id):
    project = get_object_or_404(Projects, id=id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Projet supprimé avec succès")
        return redirect('list_projects')
    return render(request, 'confirm_delete.html', {'object': project})

# CRUD pour Formations
@login_required
def list_formations(request):
    formations = Formations.objects.all()
    return render(request, 'list_formations.html', {'formations': formations})

@login_required
def delete_formation(request, id):
    formation = get_object_or_404(Formations, id=id)
    if request.method == 'POST':
        formation.delete()
        messages.success(request, "Formation supprimée avec succès")
        return redirect('list_formations')
    return render(request, 'confirm_delete.html', {'object': formation})

# CRUD pour Participation
# @login_required
# def update_participation(request, id):
#     participation = get_object_or_404(Participation, id=id)
#     if request.method == 'POST':
#         form = ParticipationForm(request.POST, instance=participation)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Participation mise à jour")
#             return redirect('gestion_utilisateurs')
#     else:
#         form = ParticipationForm(instance=participation)
#     return render(request, 'edit_participation.html', {'form': form})

def update_categ(request, id):
    categ = get_object_or_404(Project_Categ, id=id)
    if request.method == 'POST':
        form = Project_Categform(request.POST, instance=categ)
        if form.is_valid():
            print('save')
            form.save()
            messages.success(request, "Catégorie mise à jour avec succès")
            return redirect('admin_dashbord')  # Ou une autre vue appropriée
    else:
        form = Project_Categform(instance=categ)
    
    return render(request, 'categ_create.html', {'form': form,'object': categ})


### 2. Pour le modèle Technologies


def update_tech(request, id):
    tech = get_object_or_404(Technologies, id=id)
    if request.method == 'POST':
        form = TechnologiesForm(request.POST, instance=tech)
        if form.is_valid():
            form.save()
            messages.success(request, "Technologie mise à jour avec succès")
            return redirect('admin_dashbord')
    else:
        form = TechnologiesForm(instance=tech)
    
    return render(request, 'tech_create.html', {'form': form,'object': tech})


### 3. Pour le modèle Projects


def update_project(request, id):
    project = get_object_or_404(Projects, id=id)
    tech = Technologies.objects.all()
    current_techs = Tech_Project.objects.filter(Project=project).values_list('Technologies_id', flat=True)
    
    if request.method == 'POST':
        form = ProjectsForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            # Supprimer les anciennes technologies
            Tech_Project.objects.filter(Project=project).delete()
            # Ajouter les nouvelles
            for tech_id in request.POST.getlist('categories'):
                Tech_Project.objects.create(
                    Project=project,
                    Technologies_id=tech_id
                )
            messages.success(request, "Projet mis à jour avec succès")
            return redirect('admin_dashbord')
    else:
        form = ProjectsForm(instance=project)
    
    return render(request, 'create_projet.html', {
        'form': form,
        'tech': tech,
        'current_techs': current_techs,
        'object': project,
    })


### 4. Pour le modèle Formations


def update_formation(request, pk):
    formation = get_object_or_404(Formations, pk=pk)
    if request.method == 'POST':
        form = FormationForm(request.POST, request.FILES, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, "Formation mise à jour avec succès")
            return redirect('admin_dashbord')
    else:
        form = FormationForm(instance=formation)
    
    return render(request, 'admin.html', {'form': form,'object':formation})


### 5. Pour le modèle Participation


def participation(request): 
    p = Participation.objects.all()
    return render(request,'list_perticipation.html', {'p':p})

def update_participation(request, id):
    participation = get_object_or_404(Participation, id=id)
    if request.method == 'POST':
        paye = request.POST.get('paye') == 'on'
        participation.paye = paye
        participation.save()
        messages.success(request, "Participation mise à jour avec succès")
        return redirect('admin_dashbord')
    
    return redirect('participation')


from django.views.generic import ListView
from django.urls import reverse

def ParticipationListView(request):
        form = Formations.objects.filter(    participation__isnull=False ).order_by('-date_debut').distinct() 
        part = Participation.objects.all()
        data = []
        for i in form :
            data.append( {
                'form' : i,
                'attestation':Participation.objects.filter(formation = i)[0].attestation
                } )
        
        return render(request,'participations_list.html', {'form': data})
@login_required
def upload_attestation(request, f_id):
    fromation = get_object_or_404(Formations, id=f_id)
    
    if request.method == 'POST':       
        for p in Participation.objects.all(): 
             p.attestation = request.FILES['attestation']
             p.save()
        messages.success(request, "Attestation mise à jour avec succès")
        return redirect('participations_list')
    else:
        form = Formations(instance=fromation)
    
    return render(request, 'upload_attestation.html', {'form': form, 'participation': fromation})


