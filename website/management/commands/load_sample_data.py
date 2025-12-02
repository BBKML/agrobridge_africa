from django.core.management.base import BaseCommand
from website.models import PageContent, Product, Service

class Command(BaseCommand):
    help = 'Charge les données d\'exemple dans la base de données'

    def handle(self, *args, **options):
        # Créer les contenus de page
        page_contents = [
            {
                'section': 'hero',
                'title': 'AgroBridge Africa',
                'subtitle': 'Connecting Africa\'s finest harvests to the world',
                'description': 'Nous relions les meilleures récoltes africaines au monde. Transparence, qualité et impact durable.'
            },
            {
                'section': 'features',
                'title': 'Pourquoi choisir AgroBridge Africa ?',
                'subtitle': 'Nos forces',
                'description': 'Transparence, Qualité et Impact sont nos trois piliers'
            },
            {
                'section': 'products_intro',
                'title': 'Nos Produits',
                'subtitle': 'Produits agricoles africains premium',
                'description': 'Découvrez notre sélection de cacao, café et noix de cajou provenant directement des meilleures régions d\'Afrique.'
            },
            {
                'section': 'gallery',
                'title': 'Notre Travail en Images',
                'subtitle': 'Galerie',
                'description': 'Voyez comment nous travaillons avec les producteurs locaux pour vous offrir les meilleurs produits.'
            },
            {
                'section': 'cta',
                'title': 'Prêt à démarrer ?',
                'subtitle': 'Rejoignez-nous',
                'description': 'Rejoignez-nous dans notre mission de connecter les meilleurs producteurs africains aux marchés internationaux.'
            },
            {
                'section': 'about',
                'title': 'À propos d\'AgroBridge Africa',
                'subtitle': 'Notre mission',
                'description': 'Créer un impact positif en facilitant le commerce équitable entre les producteurs africains et le marché mondial.'
            },
            {
                'section': 'services_intro',
                'title': 'Nos Services',
                'subtitle': 'Solutions complètes pour le commerce agricole',
                'description': 'Des solutions complètes pour faciliter votre commerce agricole international.'
            }
        ]

        for content_data in page_contents:
            obj, created = PageContent.objects.update_or_create(
                section=content_data['section'],
                defaults={
                    'title': content_data['title'],
                    'subtitle': content_data.get('subtitle', ''),
                    'description': content_data.get('description', '')
                }
            )
            status = 'créé' if created else 'mis à jour'
            self.stdout.write(self.style.SUCCESS(f'✓ PageContent "{obj.get_section_display()}" {status}'))

        # Créer les produits
        products = [
            {
                'name': 'Fèves de cacao',
                'name_en': 'Cocoa Beans',
                'description': 'Fèves de cacao premium d\'Afrique de l\'Ouest, fermentées et séchées selon les meilleures pratiques pour garantir une qualité exceptionnelle. Nos fèves proviennent directement de coopératives certifiées.',
                'features': 'Fermentation artisanale\nCertification commerce équitable\nSéchage traditionnel\nEmballage écologique\nTraçabilité complète',
                'order': 1,
                'is_active': True
            },
            {
                'name': 'Grains de café',
                'name_en': 'Coffee Beans',
                'description': 'Café arabica et robusta de haute qualité, cultivé dans les meilleures régions d\'Afrique avec un soin particulier. Chaque grain est sélectionné pour son arôme et sa saveur.',
                'features': 'Arabica et Robusta premium\nRécolte manuelle\nRôtissage artisanal\nArome riche et complexe\nCommerçable immédiatement',
                'order': 2,
                'is_active': True
            },
            {
                'name': 'Noix de cajou',
                'name_en': 'Cashew Nuts',
                'description': 'Noix de cajou brutes et transformées, sélectionnées pour leur qualité exceptionnelle et leur conformité aux normes internationales. Croquantes et savoureuses.',
                'features': 'Noix brutes et grillées\nTraitement à froid\nSans conservateurs\nEmballage sous vide\nConserve 12 mois',
                'order': 3,
                'is_active': True
            }
        ]

        for product_data in products:
            obj, created = Product.objects.update_or_create(
                name=product_data['name'],
                defaults={
                    'name_en': product_data['name_en'],
                    'description': product_data['description'],
                    'features': product_data['features'],
                    'order': product_data['order'],
                    'is_active': product_data['is_active']
                }
            )
            status = 'créé' if created else 'mis à jour'
            self.stdout.write(self.style.SUCCESS(f'✓ Produit "{obj.name}" {status}'))

        # Créer les services
        services = [
            {
                'name': 'Mise en relation cacao',
                'icon': '🍫',
                'description': 'Connexion directe avec les meilleurs producteurs de cacao d\'Afrique de l\'Ouest. Nous garantissons une qualité supérieure et une traçabilité complète.',
                'features': 'Producteurs vérifiés\nQualité garantie\nLivraison fiable\nSupport logistique',
                'order': 1,
                'is_active': True
            },
            {
                'name': 'Mise en relation café',
                'icon': '☕',
                'description': 'Accès aux grains de café de qualité premium cultivés dans les régions les plus prestigieuses d\'Afrique.',
                'features': 'Variétés sélectionnées\nCertifications multiples\nSacs de 50kg ou 70kg\nEmballage premium',
                'order': 2,
                'is_active': True
            },
            {
                'name': 'Mise en relation noix de cajou',
                'icon': '🥜',
                'description': 'Noix de cajou sélectionnées avec soin auprès des meilleures coopératives d\'Afrique de l\'Ouest.',
                'features': 'Calibrage précis\nTraitement hygiénique\nContrôle qualité strict\nCertification sanitaire',
                'order': 3,
                'is_active': True
            },
            {
                'name': 'Facilitation d\'export',
                'icon': '🚢',
                'description': 'Accompagnement complet dans vos démarches d\'exportation. Nous gérons la documentation, le transport et la douane.',
                'features': 'Gestion documentaire\nLogistique optimisée\nClairance douanière\nAssurance transport',
                'order': 4,
                'is_active': True
            },
            {
                'name': 'Vérifications qualité',
                'icon': '✅',
                'description': 'Contrôle qualité rigoureux selon les standards internationaux. Chaque lot est certifié avant expédition.',
                'features': 'Tests laboratoire\nCertification SQF\nConformité normes ISO\nRapports détaillés',
                'order': 5,
                'is_active': True
            }
        ]

        for service_data in services:
            obj, created = Service.objects.update_or_create(
                name=service_data['name'],
                defaults={
                    'icon': service_data['icon'],
                    'description': service_data['description'],
                    'features': service_data['features'],
                    'order': service_data['order'],
                    'is_active': service_data['is_active']
                }
            )
            status = 'créé' if created else 'mis à jour'
            self.stdout.write(self.style.SUCCESS(f'✓ Service "{obj.name}" {status}'))

        self.stdout.write(self.style.SUCCESS('\n✨ Toutes les données d\'exemple ont été chargées avec succès !'))
        self.stdout.write(self.style.WARNING('\n⚠️  Note: Les images doivent être ajoutées manuellement via le dashboard ou l\'admin.'))
