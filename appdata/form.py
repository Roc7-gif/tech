from django import forms
from .models import *
from datetime import date
import os

class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ( 'attestation',)
        widgets = {
            'attestation': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class Userform(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
        }
        
        error_messages = {
            'username': {
                'required': "Le nom d'utilisateur est obligatoire.",
                'unique': "Ce nom d'utilisateur est déjà pris."
            },
            'email': {
                'invalid': "Veuillez entrer une adresse email valide.",
                'unique': "Cette adresse email est déjà utilisée."
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des messages d'erreur pour les champs obligatoires
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    def clean(self) :
                cleaned_data = super().clean() 
                Nom=cleaned_data["first_name"]
                Prenom=cleaned_data["last_name"]
                username=cleaned_data["username"]
                email=cleaned_data["email"]
                password1=cleaned_data["password1"]
                if len(username)<3:
                    self.add_error ('username','Username trop cours')
                if len(Nom)<3:
                     self.add_error ('first_name','Nom trop cours')

                if len(Prenom)<3:
                     self.add_error ('last_name','Prénom trop cours')
                for i in User.objects.all() :
                    if i.email==email:
                        message= "Email attribué à un autre compte" 
                        self.add_error ('email',message)
                return cleaned_data
                

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formations
        fields = ('title', 'description', 'image', 'statut', 'date_debut', 'date_fin','heure','place','price','categorie')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure': forms.TextInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control','type': 'number'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pré-remplissage des valeurs par défaut
        self.fields['date_debut'].initial = date.today()
        self.fields['statut'].initial = 'Bientôt'
        self.fields['description'].required = False 
        
        # Ajout des classes CSS
        for field in self.fields:
            if field not in ['statut', 'date_debut', 'date_fin']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        image = cleaned_data.get('image')
        description = cleaned_data.get('description')
        categorie = cleaned_data.get('categorie')
        
        # Validation des dates
        if date_debut and date_fin and date_fin < date_debut:
            self.add_error('date_fin', "La date de fin doit être postérieure à la date de début")
        
        # Validation de la taille de l'image
        if image:
            if image.size > 5*1024*1024:  # 5MB
                self.add_error('image', "La taille de l'image ne doit pas dépasser 5MB")
      
        return cleaned_data
class Project_Categform(forms.ModelForm) : 
    class Meta : 
        model = Project_Categ
        fields = ('Title',)
    def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields : 
                self.fields[field].widget.attrs.update({'class': 'form-control'})
                name = "Categorie de projet"
                self.name =name 


class TechnologiesForm(forms.ModelForm) : 
    class Meta : 
        model = Technologies
        fields = ('Title',)
        widget = {
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
             
        } 

    def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields : 
                self.fields[field].widget.attrs.update({'class': 'form-control'})
                name = "Technologie de projet"
                self.name =name 
            


class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ('title', 'description', 'image', 'category', )
        widgets = {

            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        
        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)            
            # Ajout des classes CSS
            for field in self.fields:
                if field not in ['category']:
                    self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        description = cleaned_data.get('description')
        category = cleaned_data.get('category')
        # Validation de la taille de l'image

        if image:
            if image.size > 10*1024*1024:  # 5MB
                self.add_error('image', "La taille de l'image ne doit pas dépasser 10MB")
      
        return cleaned_data
