"""Seed the database with categories, products, and an admin user."""
from app import create_app
from app.extensions import db
from app.models import User, Category, Product, Review

app = create_app()

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ---- Admin User ----
        admin = User(
            username='admin',
            email='admin@smartwatches.com',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # ---- Demo Customer ----
        customer = User(
            username='johndoe',
            email='john@example.com',
            first_name='John',
            last_name='Doe'
        )
        customer.set_password('password123')
        db.session.add(customer)

        # ---- Categories ----
        categories = {
            'sport': Category(
                name='Sport',
                slug='sport',
                description='Rugged smart watches built for athletes and adventurers.',
                image_url='https://images.unsplash.com/photo-1557438159-51eec7a6c9e8?w=600&q=80'
            ),
            'luxury': Category(
                name='Luxury',
                slug='luxury',
                description='Premium timepieces that blend elegance with technology.',
                image_url='https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&q=80'
            ),
            'smart': Category(
                name='Smart',
                slug='smart',
                description='Feature-rich smart watches for the connected lifestyle.',
                image_url='https://images.unsplash.com/photo-1546868871-af0de0ae72be?w=600&q=80'
            ),
            'classic': Category(
                name='Classic',
                slug='classic',
                description='Timeless designs with modern smart capabilities.',
                image_url='https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600&q=80'
            )
        }
        for cat in categories.values():
            db.session.add(cat)
        db.session.flush()

        # ---- Products ----
        products = [
            Product(
                name='Apex Pro X1',
                slug='apex-pro-x1',
                description='The Apex Pro X1 represents the pinnacle of sports watch engineering. Featuring a titanium case, sapphire crystal display, and 100m water resistance, this watch is built for extreme conditions. Advanced heart rate monitoring, GPS tracking, and a 14-day battery life make it the ultimate companion for serious athletes.',
                short_description='Titanium sports watch with GPS and 14-day battery',
                price=599.00,
                compare_price=749.00,
                stock=25,
                sku='SW-APEX-001',
                category_id=categories['sport'].id,
                image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80',
                image_url_2='https://images.unsplash.com/photo-1557438159-51eec7a6c9e8?w=600&q=80',
                image_url_3='https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&q=80',
                is_featured=True,
                brand='Chronos',
                specifications='Case: 46mm Titanium\nDisplay: AMOLED Sapphire Crystal\nWater Resistance: 100m\nBattery: 14 days\nSensors: HR, SpO2, GPS, Altimeter\nWeight: 52g'
            ),
            Product(
                name='Meridian Elite',
                slug='meridian-elite',
                description='The Meridian Elite is where haute horlogerie meets cutting-edge technology. Hand-finished stainless steel case with genuine leather strap, this watch features a stunning always-on display, NFC payments, and seamless smartphone integration. Perfect for the discerning professional.',
                short_description='Luxury smart watch with leather strap and NFC payments',
                price=899.00,
                compare_price=1099.00,
                stock=15,
                sku='SW-MERI-002',
                category_id=categories['luxury'].id,
                image_url='https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&q=80',
                image_url_2='https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600&q=80',
                image_url_3='https://images.unsplash.com/photo-1509048191080-d2984bad6ae5?w=600&q=80',
                is_featured=True,
                brand='Aurelian',
                specifications='Case: 42mm Stainless Steel\nDisplay: AMOLED Always-On\nStrap: Italian Leather\nBattery: 5 days\nFeatures: NFC, Bluetooth 5.2\nWeight: 48g'
            ),
            Product(
                name='Vanguard Series 7',
                slug='vanguard-series-7',
                description='The Vanguard Series 7 pushes the boundaries of what a smart watch can do. With its edge-to-edge retina display, blood oxygen monitoring, ECG capability, and fall detection, it is the most health-focused watch in our collection. Stay connected with calls, messages, and apps right from your wrist.',
                short_description='Advanced health monitoring with ECG and blood oxygen',
                price=449.00,
                compare_price=0,
                stock=40,
                sku='SW-VANG-003',
                category_id=categories['smart'].id,
                image_url='https://images.unsplash.com/photo-1667211586479-3846af286124?q=80&w=765&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                image_url_2='https://images.unsplash.com/photo-1667211586479-3846af286124?q=80&w=765&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                image_url_3='https://images.unsplash.com/photo-1667211586479-3846af286124?q=80&w=765&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                is_featured=True,
                brand='TechForge',
                specifications='Case: 44mm Aluminum\nDisplay: Retina LTPO OLED\nHealth: ECG, SpO2, HR\nBattery: 36 hours\nOS: WatchOS 10\nWeight: 38g'
            ),
            Product(
                name='Heritage Chronograph',
                slug='heritage-chronograph',
                description='The Heritage Chronograph pays homage to traditional watchmaking while embracing modern technology. The classic dial design houses discreet smart features including step counting, sleep tracking, and notification alerts. A watch that commands respect in any boardroom.',
                short_description='Classic chronograph design with discreet smart features',
                price=699.00,
                compare_price=849.00,
                stock=20,
                sku='SW-HERI-004',
                category_id=categories['classic'].id,
                image_url='https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600&q=80',
                image_url_2='https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&q=80',
                image_url_3='https://images.unsplash.com/photo-1507679799987-c73b7651af56?w=600&q=80',
                is_featured=True,
                brand='Montecello',
                specifications='Case: 40mm Stainless Steel\nDial: Analog + Hidden OLED\nStrap: Genuine Leather\nBattery: 30 days\nFeatures: Steps, Sleep, Notifications\nWeight: 62g'
            ),
            Product(
                name='Titan Endurance',
                slug='titan-endurance',
                description='Built for ultra-marathoners and triathletes, the Titan Endurance features multi-sport GPS tracking, advanced running dynamics, and training load analysis. The reinforced polymer case withstands extreme temperatures and impacts while remaining incredibly lightweight.',
                short_description='Ultra-endurance sports watch with multi-sport GPS',
                price=549.00,
                compare_price=0,
                stock=30,
                sku='SW-TITN-005',
                category_id=categories['sport'].id,
                image_url='https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&q=80',
                image_url_2='https://images.unsplash.com/photo-1557438159-51eec7a6c9e8?w=600&q=80',
                image_url_3='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80',
                is_featured=True,
                brand='Chronos',
                specifications='Case: 47mm Reinforced Polymer\nDisplay: MIP Sunlight-Readable\nGPS: Multi-Band GNSS\nBattery: 21 days\nSensors: HR, Compass, Barometer\nWeight: 44g'
            ),
            Product(
                name='Celestia Rose Gold',
                slug='celestia-rose-gold',
                description='The Celestia in rose gold is a statement of refined luxury. Diamond-cut bezel, mother-of-pearl dial accents, and an interchangeable mesh bracelet make this the most elegant smart watch in our collection. Features health tracking, music control, and customizable watch faces.',
                short_description='Rose gold luxury watch with diamond-cut bezel',
                price=1299.00,
                compare_price=1599.00,
                stock=8,
                sku='SW-CELS-006',
                category_id=categories['luxury'].id,
                image_url='https://images.unsplash.com/photo-1509048191080-d2984bad6ae5?w=600&q=80',
                image_url_2='https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&q=80',
                image_url_3='https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600&q=80',
                is_featured=True,
                brand='Aurelian',
                specifications='Case: 38mm Rose Gold PVD\nBezel: Diamond-Cut\nDisplay: AMOLED 454x454\nStrap: Milanese Mesh\nBattery: 4 days\nWeight: 40g'
            ),
            Product(
                name='Nexus Ultra',
                slug='nexus-ultra',
                description='The Nexus Ultra is the most connected smart watch we offer. Featuring LTE connectivity, you can make calls, stream music, and use apps without your phone. The ultra-bright display is readable in direct sunlight, and the all-day battery keeps you going from dawn to midnight.',
                short_description='LTE-connected smart watch with standalone capability',
                price=499.00,
                compare_price=599.00,
                stock=35,
                sku='SW-NEXS-007',
                category_id=categories['smart'].id,
                image_url='https://images.unsplash.com/photo-1667211586479-3846af286124?q=80&w=765&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                image_url_2='https://images.unsplash.com/photo-1667211586479-3846af286124?q=80&w=765&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                image_url_3='https://images.unsplash.com/photo-1667211586479-3846af286124?q=80&w=765&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                is_featured=True,
                brand='TechForge',
                specifications='Case: 45mm Aluminum\nDisplay: AMOLED 1.4" 500nits\nConnectivity: LTE, WiFi, BT 5.2\nBattery: 24 hours (LTE)\nStorage: 32GB\nWeight: 42g'
            ),
            Product(
                name='Artisan Automatic',
                slug='artisan-automatic',
                description='The Artisan Automatic combines a genuine Swiss automatic movement with smart notification capabilities. The exhibition caseback reveals the intricate mechanical movement, while the sapphire crystal front conceals a subtle OLED display for incoming alerts. Limited edition of 500 pieces.',
                short_description='Swiss automatic movement with smart notifications',
                price=1899.00,
                compare_price=2299.00,
                stock=5,
                sku='SW-ARTS-008',
                category_id=categories['classic'].id,
                image_url='https://images.unsplash.com/photo-1507679799987-c73b7651af56?w=600&q=80',
                image_url_2='https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600&q=80',
                image_url_3='https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&q=80',
                is_featured=True,
                brand='Montecello',
                specifications='Case: 41mm 316L Stainless Steel\nMovement: Swiss Automatic + Smart\nCrystal: Sapphire (front & back)\nWater Resistance: 50m\nEdition: Limited 500 pieces\nWeight: 75g'
            ),
        ]

        for product in products:
            db.session.add(product)

        db.session.flush()

        # ---- Sample Reviews ----
        reviews = [
            Review(user_id=customer.id, product_id=products[0].id, rating=5,
                   title='Best sports watch I have owned',
                   comment='The battery life is incredible and the GPS accuracy is spot on. Worth every penny.'),
            Review(user_id=customer.id, product_id=products[1].id, rating=5,
                   title='Stunning craftsmanship',
                   comment='This watch gets compliments everywhere I go. The leather strap is buttery soft.'),
            Review(user_id=customer.id, product_id=products[2].id, rating=4,
                   title='Great health features',
                   comment='The ECG and blood oxygen monitoring have been very accurate. Battery could be better.'),
            Review(user_id=customer.id, product_id=products[3].id, rating=5,
                   title='Perfect blend of classic and smart',
                   comment='Nobody can tell this is a smart watch until I show them the hidden display. Brilliant design.'),
        ]

        for review in reviews:
            db.session.add(review)

        db.session.commit()
        print('Database seeded successfully!')
        print(f'Admin login: admin@smartwatches.com / admin123')
        print(f'Customer login: john@example.com / password123')
        print(f'Created {len(products)} products across {len(categories)} categories')


if __name__ == '__main__':
    seed()
