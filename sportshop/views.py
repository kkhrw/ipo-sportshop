from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    """Главная страница со ссылками"""
    content = """
    <h1>Добро пожаловать в интернет-магазин спортивных товаров и питания!</h1>
    <p>Выберите раздел:</p>
    <ul>
        <li><a href="/about/">Информация об авторе</a></li>
        <li><a href="/info/">Информация о магазине (Магазин зона спорта)</a></li>
    </ul>
    """
    return HttpResponse(content)

def about(request):
    """Страница об авторе"""
    
    author_name = "Короленко Ульяна Сергеевна"
    group = "Группа 87 Тп"
    content = f"""
    <h1>Информация об авторе</h1>
    <p><strong>ФИО:</strong> {author_name}</p>
    <p><strong>Группа:</strong> {group}</p>
    """
    return HttpResponse(content)

def shop_info(request):
    """Страница о спортивном магазине"""
    # ТАБЛИЦА ВЫШЕ НЕ ВИДНА, ПОЭТОМУ Я ПИШУ ПРИМЕР. 
    # ЗАМЕНИТЕ 'Электроника' НА ВАШУ ТЕМУ.
    shop_theme = "Магазин сспортивных товаров и питания" 
    description = "В данном проекте реализуется функционал интернет-магазина спортивных товаров и питания"
    
    content = f"""
    <h1>О магазине</h1>
    <h2>Тема лабораторной работы: {shop_theme}</h2>
    <p>{description}</p>
    <p>Здесь будут представлены товары, корзина и система заказов.</p>
    """
    return HttpResponse(content)
