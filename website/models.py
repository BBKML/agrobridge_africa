# ============================================
# 5. website/models.py
# ============================================

from django.db import models
from django.contrib.auth.models import User

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d/%m/%Y')}"


class PageContent(models.Model):
    """Stocke les contenus éditables du site"""
    SECTION_CHOICES = [
        ('hero', 'Section Hero'),
        ('features', 'Nos forces'),
        ('products_intro', 'Intro Produits'),
        ('gallery', 'Galerie'),
        ('cta', 'Appel à l\'action'),
        ('about', 'À propos'),
        ('services_intro', 'Intro Services'),
    ]
    
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='content/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Contenu de page'
        verbose_name_plural = 'Contenus de page'
    
    def __str__(self):
        return f"{self.get_section_display()}"


class Product(models.Model):
    """Produits avec infos éditables"""
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, blank=True, help_text="Nom en anglais")
    description = models.TextField()
    features = models.TextField(help_text="Caractéristiques (une par ligne)")
    image = models.ImageField(upload_to='products/')
    order = models.IntegerField(default=0, help_text="Ordre d'affichage")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
    
    def __str__(self):
        return self.name


class Service(models.Model):
    """Services avec infos éditables"""
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    description = models.TextField()
    features = models.TextField(help_text="Caractéristiques (une par ligne)")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.name



