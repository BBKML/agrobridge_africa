# ============================================
# 4. website/views.py
# ============================================

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from .models import ContactMessage, PageContent, Product, Service
from .utils.images import generate_variants

def home(request):
    contents = {obj.section: obj for obj in PageContent.objects.all()}
    products = Product.objects.filter(is_active=True)
    return render(request, 'website/home.html', {'contents': contents, 'products': products})

def about(request):
    contents = {obj.section: obj for obj in PageContent.objects.all()}
    return render(request, 'website/about.html', {'contents': contents})

def services(request):
    contents = {obj.section: obj for obj in PageContent.objects.all()}
    services_list = Service.objects.filter(is_active=True)
    return render(request, 'website/services.html', {'services': services_list, 'contents': contents})

def products(request):
    contents = {obj.section: obj for obj in PageContent.objects.all()}
    products_list = Product.objects.filter(is_active=True)
    return render(request, 'website/products.html', {'products': products_list, 'contents': contents})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message_text = request.POST.get('message')
        
        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message_text
            )
            messages.success(request, 'Merci ! Votre message a été reçu. Nous vous répondrons bientôt.')
            return redirect('website:contact')
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')
        
    return render(request, 'website/contact.html')


# ========== DASHBOARD & ADMIN ==========

@login_required
def dashboard(request):
    """Vue principale du dashboard"""
    if not request.user.is_staff:
        messages.error(request, "Accès refusé.")
        return redirect('website:home')
    
    stats = {
        'messages_total': ContactMessage.objects.count(),
        'messages_unread': ContactMessage.objects.filter(is_read=False).count(),
        'products_count': Product.objects.count(),
        'services_count': Service.objects.count(),
    }
    
    recent_messages = ContactMessage.objects.all()[:5]
    
    return render(request, 'website/dashboard.html', {
        'stats': stats,
        'recent_messages': recent_messages
    })


@login_required
def content_edit(request, section):
    """Édition des contenus de page"""
    if not request.user.is_staff:
        return redirect('website:home')
    
    content, created = PageContent.objects.get_or_create(section=section)
    
    if request.method == 'POST':
        content.title = request.POST.get('title', content.title)
        content.subtitle = request.POST.get('subtitle', content.subtitle)
        content.description = request.POST.get('description', content.description)
        
        if 'image' in request.FILES:
            content.image = request.FILES['image']
        
        content.save()
        # generate image variants (best-effort)
        try:
            if content.image and getattr(content.image, 'path', None):
                generate_variants(content.image.path)
        except Exception:
            pass
        messages.success(request, f"Section '{content.get_section_display()}' mise à jour.")
        return redirect('website:dashboard')
    
    return render(request, 'website/content_edit.html', {'content': content})


@login_required
def products_manage(request):
    """Gestion des produits"""
    if not request.user.is_staff:
        return redirect('website:home')
    
    products = Product.objects.all()
    return render(request, 'website/products_manage.html', {'products': products})


@login_required
def product_edit(request, pk=None):
    """Édition d'un produit"""
    if not request.user.is_staff:
        return redirect('website:home')
    
    product = get_object_or_404(Product, pk=pk) if pk else None
    
    if request.method == 'POST':
        if not product:
            product = Product()
        
        product.name = request.POST.get('name')
        product.name_en = request.POST.get('name_en', '')
        product.description = request.POST.get('description')
        product.features = request.POST.get('features')
        product.order = int(request.POST.get('order', 0))
        product.is_active = request.POST.get('is_active') == 'on'
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        elif not product.pk:
            messages.error(request, "Une image est requise pour créer un produit.")
            return render(request, 'website/product_edit.html', {'product': product})

        product.save()

        # generate image variants (best-effort)
        try:
            if product.image and getattr(product.image, 'path', None):
                generate_variants(product.image.path)
        except Exception:
            pass

        messages.success(request, f"Produit '{product.name}' enregistré.")
        return redirect('website:products_manage')
    
    return render(request, 'website/product_edit.html', {'product': product})


@login_required
def product_delete(request, pk):
    """Suppression d'un produit"""
    if not request.user.is_staff:
        return redirect('website:home')
    
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, f"Produit supprimé.")
    return redirect('website:products_manage')


@login_required
def messages_view(request):
    """Liste des messages de contact"""
    if not request.user.is_staff:
        return redirect('website:home')
    
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'unread':
        messages_list = ContactMessage.objects.filter(is_read=False)
    else:
        messages_list = ContactMessage.objects.all()
    
    return render(request, 'website/messages_view.html', {
        'messages': messages_list,
        'filter_type': filter_type
    })


@login_required
@require_http_methods(["GET", "POST"])
def message_detail(request, pk):
    """Détail d'un message"""
    if not request.user.is_staff:
        return redirect('website:home')
    
    message_obj = get_object_or_404(ContactMessage, pk=pk)
    
    if not message_obj.is_read:
        message_obj.is_read = True
        message_obj.save()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            message_obj.delete()
            messages.success(request, "Message supprimé.")
            return redirect('website:messages_view')
    
    return render(request, 'website/message_detail.html', {'message': message_obj})


@login_required
def services_manage(request):
    """Gestion des services"""
    if not request.user.is_staff:
        return redirect('website:home')
    
    services = Service.objects.all()
    return render(request, 'website/services_manage.html', {'services': services})


@login_required
def service_edit(request, pk=None):
    """Édition d'un service"""
    if not request.user.is_staff:
        return redirect('website:home')
    
    service = get_object_or_404(Service, pk=pk) if pk else None
    
    if request.method == 'POST':
        if not service:
            service = Service()
        
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.features = request.POST.get('features')
        service.order = int(request.POST.get('order', 0))
        service.is_active = request.POST.get('is_active') == 'on'
        # handle image upload if provided
        if 'image' in request.FILES:
            service.image = request.FILES['image']

        service.save()

        # generate image variants (best-effort)
        try:
            if service.image and getattr(service.image, 'path', None):
                generate_variants(service.image.path)
        except Exception:
            pass

        messages.success(request, f"Service '{service.name}' enregistré.")
        return redirect('website:services_manage')
    
    return render(request, 'website/service_edit.html', {'service': service})


@login_required
def service_delete(request, pk):
    """Suppression d'un service"""
    if not request.user.is_staff:
        return redirect('website:home')
    
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.success(request, "Service supprimé.")
    return redirect('website:services_manage')
