from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Manufacturer, Product, Cart, CartItem
from decimal import Decimal


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Начинаю заполнение базы данных...'))
        
        # Очистка старых данных
        self.stdout.write('Очистка старых данных...')
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Manufacturer.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # === СОЗДАНИЕ ПРОИЗВОДИТЕЛЕЙ (5 шт.) ===
        self.stdout.write('Создание производителей...')
        manufacturers_data = [
            {"name": "Nike", "country": "США", "description": "Американский производитель спортивной одежды и обуви"},
            {"name": "Adidas", "country": "Германия", "description": "Немецкий производитель спортивных товаров"},
            {"name": "Puma", "country": "Германия", "description": "Производитель спортивной обуви и одежды"},
            {"name": "Reebok", "country": "США", "description": "Американский бренд спортивной обуви и одежды"},
            {"name": "Under Armour", "country": "США", "description": "Производитель спортивной экипировки"},
        ]
        
        manufacturers = []
        for m_data in manufacturers_data:
            manufacturer = Manufacturer.objects.create(**m_data)
            manufacturers.append(manufacturer)
        
        # === СОЗДАНИЕ КАТЕГОРИЙ (10 шт.) ===
        self.stdout.write('Создание категорий...')
        categories_data = [
            {"name": "Тренажеры", "description": "Силовые и кардио тренажеры для дома и зала"},
            {"name": "Велоспорт", "description": "Велосипеды и аксессуары"},
            {"name": "Фитнес", "description": "Товары для фитнеса и аэробики"},
            {"name": "Единоборства", "description": "Экипировка для боевых искусств"},
            {"name": "Туризм", "description": "Снаряжение для туризма и активного отдыха"},
            {"name": "Плавание", "description": "Товары для плавания"},
            {"name": "Бег", "description": "Обувь и одежда для бега"},
            {"name": "Командные виды спорта", "description": "Мячи и инвентарь для командных игр"},
            {"name": "Зимний спорт", "description": "Товары для зимних видов спорта"},
            {"name": "Спортивное питание", "description": "Протеины, витамины и добавки"},
        ]
        
        categories = []
        for c_data in categories_data:
            category = Category.objects.create(**c_data)
            categories.append(category)
        
        # === СОЗДАНИЕ ТОВАРОВ (34 шт.) ===
        self.stdout.write('Создание товаров...')
        products_data = [
            # Тренажеры (4 товара)
            {"name": "Гантели разборные 20кг", "description": "Набор разборных гантелей общим весом 20кг", "price": Decimal("299.99"), "stock_quantity": 15, "category": categories[0], "manufacturer": manufacturers[0]},
            {"name": "Штанга олимпийская", "description": "Олимпийская штанга 20кг", "price": Decimal("499.99"), "stock_quantity": 8, "category": categories[0], "manufacturer": manufacturers[1]},
            {"name": "Беговая дорожка X100", "description": "Электрическая беговая дорожка с регулировкой наклона", "price": Decimal("1999.99"), "stock_quantity": 5, "category": categories[0], "manufacturer": manufacturers[4]},
            {"name": "Велотренажер магнитный", "description": "Магнитный велотренажер с компьютером", "price": Decimal("899.99"), "stock_quantity": 10, "category": categories[0], "manufacturer": manufacturers[2]},
            
            # Велоспорт (4 товара)
            {"name": "Горный велосипед 26", "description": "Горный велосипед с 21 скоростью", "price": Decimal("1299.99"), "stock_quantity": 12, "category": categories[1], "manufacturer": manufacturers[0]},
            {"name": "Шоссейный велосипед", "description": "Шоссейный велосипед для гонок", "price": Decimal("1799.99"), "stock_quantity": 6, "category": categories[1], "manufacturer": manufacturers[1]},
            {"name": "Велосипедный шлем", "description": "Защитный шлем для велоспорта", "price": Decimal("79.99"), "stock_quantity": 25, "category": categories[1], "manufacturer": manufacturers[2]},
            {"name": "Велосипедный замок", "description": "Надежный U-образный замок", "price": Decimal("39.99"), "stock_quantity": 30, "category": categories[1], "manufacturer": manufacturers[3]},
            
            # Фитнес (4 товара)
            {"name": "Коврик для йоги", "description": "Нескользящий коврик для йоги 6мм", "price": Decimal("29.99"), "stock_quantity": 50, "category": categories[2], "manufacturer": manufacturers[0]},
            {"name": "Фитнес-резинка набор", "description": "Набор из 5 резинок разной степени сопротивления", "price": Decimal("49.99"), "stock_quantity": 40, "category": categories[2], "manufacturer": manufacturers[1]},
            {"name": "Скакалка скоростная", "description": "Скоростная скакалка с подшипниками", "price": Decimal("19.99"), "stock_quantity": 35, "category": categories[2], "manufacturer": manufacturers[2]},
            {"name": "Медбол 5кг", "description": "Медицинский мяч весом 5кг", "price": Decimal("89.99"), "stock_quantity": 20, "category": categories[2], "manufacturer": manufacturers[3]},
            
            # Единоборства (3 товара)
            {"name": "Боксерские перчатки 12oz", "description": "Профессиональные боксерские перчатки", "price": Decimal("129.99"), "stock_quantity": 18, "category": categories[3], "manufacturer": manufacturers[0]},
            {"name": "Боксерский мешок", "description": "Боксерский мешок 80см", "price": Decimal("199.99"), "stock_quantity": 10, "category": categories[3], "manufacturer": manufacturers[1]},
            {"name": "Защитный шлем боксерский", "description": "Шлем для бокса и единоборств", "price": Decimal("89.99"), "stock_quantity": 15, "category": categories[3], "manufacturer": manufacturers[4]},
            
            # Туризм (4 товара)
            {"name": "Рюкзак туристический 60л", "description": "Большой рюкзак для походов", "price": Decimal("149.99"), "stock_quantity": 20, "category": categories[4], "manufacturer": manufacturers[2]},
            {"name": "Палатка 4-местная", "description": "Двухслойная палатка для кемпинга", "price": Decimal("299.99"), "stock_quantity": 8, "category": categories[4], "manufacturer": manufacturers[3]},
            {"name": "Спальный мешок", "description": "Теплый спальный мешок до -10°C", "price": Decimal("119.99"), "stock_quantity": 25, "category": categories[4], "manufacturer": manufacturers[4]},
            {"name": "Коврик туристический", "description": "Самонадувающийся коврик", "price": Decimal("59.99"), "stock_quantity": 30, "category": categories[4], "manufacturer": manufacturers[0]},
            
            # Плавание (3 товара)
            {"name": "Очки для плавания", "description": "Профессиональные очки для плавания", "price": Decimal("39.99"), "stock_quantity": 40, "category": categories[5], "manufacturer": manufacturers[1]},
            {"name": "Шапочка для плавания", "description": "Силиконовая шапочка", "price": Decimal("19.99"), "stock_quantity": 50, "category": categories[5], "manufacturer": manufacturers[2]},
            {"name": "Плавки мужские", "description": "Спортивные плавки для бассейна", "price": Decimal("29.99"), "stock_quantity": 35, "category": categories[5], "manufacturer": manufacturers[3]},
            
            # Бег (4 товара)
            {"name": "Кроссовки беговые", "description": "Профессиональные беговые кроссовки", "price": Decimal("159.99"), "stock_quantity": 22, "category": categories[6], "manufacturer": manufacturers[0]},
            {"name": "Фитнес-браслет", "description": "Умный браслет с пульсометром", "price": Decimal("99.99"), "stock_quantity": 30, "category": categories[6], "manufacturer": manufacturers[4]},
            {"name": "Пояс для бега", "description": "Беговой пояс для телефона", "price": Decimal("24.99"), "stock_quantity": 45, "category": categories[6], "manufacturer": manufacturers[1]},
            {"name": "Фонарь налобный", "description": "Светодиодный налобный фонарь", "price": Decimal("34.99"), "stock_quantity": 28, "category": categories[6], "manufacturer": manufacturers[2]},
            
            # Командные виды спорта (3 товара)
            {"name": "Футбольный мяч", "description": "Профессиональный футбольный мяч размер 5", "price": Decimal("49.99"), "stock_quantity": 25, "category": categories[7], "manufacturer": manufacturers[0]},
            {"name": "Баскетбольный мяч", "description": "Баскетбольный мяч размер 7", "price": Decimal("59.99"), "stock_quantity": 20, "category": categories[7], "manufacturer": manufacturers[1]},
            {"name": "Волейбольная сетка", "description": "Сетка для волейбола", "price": Decimal("79.99"), "stock_quantity": 12, "category": categories[7], "manufacturer": manufacturers[3]},
            
            # Зимний спорт (3 товара)
            {"name": "Лыжи горные", "description": "Горные лыжи 170см", "price": Decimal("599.99"), "stock_quantity": 7, "category": categories[8], "manufacturer": manufacturers[2]},
            {"name": "Сноуборд", "description": "Сноуборд 155см", "price": Decimal("449.99"), "stock_quantity": 9, "category": categories[8], "manufacturer": manufacturers[4]},
            {"name": "Лыжные палки", "description": "Телескопические лыжные палки", "price": Decimal("69.99"), "stock_quantity": 18, "category": categories[8], "manufacturer": manufacturers[0]},
            
            # Спортивное питание (2 товара)
            {"name": "Протеин whey 2кг", "description": "Сывороточный протеин со вкусом шоколада", "price": Decimal("89.99"), "stock_quantity": 40, "category": categories[9], "manufacturer": manufacturers[1]},
            {"name": "BCAA аминокислоты", "description": "Комплекс аминокислот BCAA 300г", "price": Decimal("49.99"), "stock_quantity": 35, "category": categories[9], "manufacturer": manufacturers[3]},
        ]
        
        products = []
        for p_data in products_data:
            product = Product.objects.create(**p_data)
            products.append(product)
        
        # === СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ (5 шт.) ===
        self.stdout.write('Создание пользователей...')
        users_data = [
            {"username": "ivan_petrov", "email": "ivan@example.com", "first_name": "Иван", "last_name": "Петров"},
            {"username": "anna_sidorova", "email": "anna@example.com", "first_name": "Анна", "last_name": "Сидорова"},
            {"username": "sergey_ivanov", "email": "sergey@example.com", "first_name": "Сергей", "last_name": "Иванов"},
            {"username": "elena_kozlova", "email": "elena@example.com", "first_name": "Елена", "last_name": "Козлова"},
            {"username": "dmitry_smirnov", "email": "dmitry@example.com", "first_name": "Дмитрий", "last_name": "Смирнов"},
        ]
        
        users = []
        for u_data in users_data:
            user = User.objects.create_user(
                username=u_data["username"],
                email=u_data["email"],
                first_name=u_data["first_name"],
                last_name=u_data["last_name"],
                password="password123"
            )
            users.append(user)
        
        # === СОЗДАНИЕ КОРЗИН ===
        self.stdout.write('Создание корзин...')
        carts = []
        for user in users:
            cart = Cart.objects.create(user=user)
            carts.append(cart)
        
        # === ДОБАВЛЕНИЕ ТОВАРОВ В КОРЗИНЫ ===
        self.stdout.write('Добавление товаров в корзины...')
        
        # Корзина Ивана: 3 товара
        CartItem.objects.create(cart=carts[0], product=products[0], quantity=2)
        CartItem.objects.create(cart=carts[0], product=products[16], quantity=1)
        CartItem.objects.create(cart=carts[0], product=products[24], quantity=1)
        
        # Корзина Анны: 2 товара
        CartItem.objects.create(cart=carts[1], product=products[8], quantity=1)
        CartItem.objects.create(cart=carts[1], product=products[9], quantity=2)
        
        # Корзина Сергея: 4 товара
        CartItem.objects.create(cart=carts[2], product=products[4], quantity=1)
        CartItem.objects.create(cart=carts[2], product=products[6], quantity=1)
        CartItem.objects.create(cart=carts[2], product=products[13], quantity=1)
        CartItem.objects.create(cart=carts[2], product=products[21], quantity=2)
        
        # Корзина Елены: 2 товара
        CartItem.objects.create(cart=carts[3], product=products[12], quantity=1)
        CartItem.objects.create(cart=carts[3], product=products[19], quantity=1)
        
        # Корзина Дмитрия: 3 товара
        CartItem.objects.create(cart=carts[4], product=products[28], quantity=1)
        CartItem.objects.create(cart=carts[4], product=products[30], quantity=1)
        CartItem.objects.create(cart=carts[4], product=products[17], quantity=1)
        
        # === СТАТИСТИКА ===
        self.stdout.write(self.style.SUCCESS('\n=== ГОТОВО! ==='))
        self.stdout.write(self.style.SUCCESS(f'Создано производителей: {Manufacturer.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Создано категорий: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Создано товаров: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Создано пользователей: {User.objects.filter(is_superuser=False).count()}'))
        self.stdout.write(self.style.SUCCESS(f'Создано корзин: {Cart.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Создано элементов корзины: {CartItem.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\nПароль для всех пользователей: password123'))