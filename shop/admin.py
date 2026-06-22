from django.contrib import admin
from .models import Category, Manufacturer, Product, Cart, CartItem, Order, OrderItem, Profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'id')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'manufacturer', 'price', 'stock_quantity', 'created_at')
    list_filter = ('category', 'manufacturer', 'created_at')
    search_fields = ('name', 'description', 'category__name', 'manufacturer__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image')
        }),
        ('Цены и наличие', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Связи', {
            'fields': ('category', 'manufacturer')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('item_cost',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_cost')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'total_cost')
    inlines = [CartItemInline]

    def total_cost(self, obj):
        return obj.total_cost()
    total_cost.short_description = "Общая стоимость"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'item_cost')
    list_filter = ('cart', 'product')
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('item_cost',)

    def item_cost(self, obj):
        return obj.item_cost()
    item_cost.short_description = "Стоимость элемента"

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_cost',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_cost', 'created_at', 'email_sent')
    list_filter = ('email_sent', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ('created_at', 'total_cost')
    inlines = [OrderItemInline]
    
    def has_add_permission(self, request):
        return False  # Заказы создаются только через оформление
    
    def has_delete_permission(self, request, obj=None):
        return False  # Заказы нельзя удалять


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'full_name', 'phone')