# ============================================
# 6. website/admin.py
# ============================================

from django.contrib import admin
from .models import ContactMessage, PageContent, Product, Service
from django.utils.html import format_html

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_read', 'created_at']
    list_filter = ['created_at', 'is_read']
    search_fields = ['name', 'email', 'message', 'phone']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Informations de contact', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('État', {
            'fields': ('is_read', 'created_at')
        }),
    )

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ['get_section_display', 'updated_at']
    list_filter = ['section', 'updated_at']
    search_fields = ['title', 'description']
    fieldsets = (
        ('Section', {
            'fields': ('section',)
        }),
        ('Contenu', {
            'fields': ('title', 'subtitle', 'description', 'image')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Produit', {
            'fields': ('name', 'name_en', 'description', 'image')
        }),
        ('Caractéristiques', {
            'fields': ('features',)
        }),
        ('Options', {
            'fields': ('order', 'is_active')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    def image_preview(self, obj):
        if getattr(obj, 'image', None):
            try:
                return format_html('<img src="{}" style="width:40px;height:40px;object-fit:cover;border-radius:4px;" />', obj.image.url)
            except Exception:
                return '-'
        return '-'

    image_preview.short_description = 'Image'

    list_display = ['name', 'image_preview', 'is_active', 'order', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Service', {
            'fields': ('name', 'image', 'description')
        }),
        ('Caractéristiques', {
            'fields': ('features',)
        }),
        ('Options', {
            'fields': ('order', 'is_active')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

