document.addEventListener('DOMContentLoaded', function() {
    console.log('Zona Sporta загружен!');

    initToasts();
    
    const productsContainer = document.getElementById('api-products-container');
    if (productsContainer) {
        loadProductsFromAPI(productsContainer);
    }
    
    // Обновляем счётчик корзины при загрузке
    if (document.querySelector('.cart-count')) {
        updateCartCount();
    }
});


function getCSRFToken() {
    // Пробуем получить из meta тега
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) return metaToken.getAttribute('content');
    
    // Пробуем получить из скрытого поля формы
    const formToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (formToken) return formToken.value;
    
    // Пробуем получить из cookie
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}

function initToasts() {
    const toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(toastEl => {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    });
}

function showNotification(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'text-bg-success' : 
                    type === 'error' ? 'text-bg-danger' : 
                    type === 'warning' ? 'text-bg-warning' : 'text-bg-info';
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center ${bgClass} border-0" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="4000">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const newToast = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(newToast);
    bsToast.show();
    
    newToast.addEventListener('hidden.bs.toast', () => {
        newToast.remove();
    });
}


function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    container.style.cssText = 'position: fixed; top: 80px; right: 20px; z-index: 1050;';
    document.body.appendChild(container);
    return container;
}

async function loadProductsFromAPI(container) {
    container.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
            <p class="mt-3 text-muted">Загрузка товаров...</p>
        </div>
    `;
    
    try {
        const response = await fetch('/api/products/', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
            credentials: 'same-origin' 
        });
        
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        container.innerHTML = '';
        
        if (data.results && data.results.length > 0) {
            data.results.forEach(product => {
                const productCard = createProductCard(product);
                container.insertAdjacentHTML('beforeend', productCard);
            });
        } else if (data.length > 0) {
            // Если нет results, значит пагинации нет
            data.forEach(product => {
                const productCard = createProductCard(product);
                container.insertAdjacentHTML('beforeend', productCard);
            });
        } else {
            container.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-info text-center">
                        Товары не найдены
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Ошибка загрузки товаров:', error);
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger text-center">
                    Не удалось загрузить товары. Пожалуйста, попробуйте позже.
                </div>
            </div>
        `;
        showNotification('Ошибка загрузки товаров', 'error');
    }
}


function createProductCard(product) {
    const imageUrl = product.image_url || '';
    const imageHTML = imageUrl 
        ? `<img src="${imageUrl}" class="card-img-top" alt="${product.name}" style="height: 200px; object-fit: cover;">`
        : `<div class="card-img-top d-flex align-items-center justify-content-center bg-light" style="height: 200px;">
             <i class="bi bi-image" style="font-size: 3rem; color: #ccc;"></i>
           </div>`;
    
    return `
        <div class="col-sm-6 col-md-4 col-lg-4">
            <div class="card h-100">
                ${imageHTML}
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text text-muted small flex-grow-1">
                        ${product.description ? product.description.substring(0, 60) + '...' : ''}
                    </p>
                    <div class="mb-2">
                        <span class="category-badge">${product.category_name || 'Без категории'}</span>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-auto">
                        <span class="price-tag">${product.price} руб.</span>
                        <a href="/catalog/${product.id}/" class="btn btn-primary btn-sm">
                            Подробнее
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
}


// ГЛОБАЛЬНАЯ функция для добавления в корзину
window.addToCart = async function(productId) {
    const csrfToken = getCSRFToken();
    
    if (!csrfToken) {
        showNotification('Ошибка безопасности. Обновите страницу.', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/cart-items/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'Accept': 'application/json',
            },
            credentials: 'same-origin',
            body: JSON.stringify({
                product: productId,
                quantity: 1
            })
        });
        
        if (response.ok) {
            showNotification('Товар успешно добавлен в корзину!', 'success');
            updateCartCount();
        } else {
            const errorData = await response.json();
            const errorMessage = errorData.detail || errorData.quantity || 'Не удалось добавить товар';
            showNotification(`Ошибка: ${errorMessage}`, 'error');
        }
    } catch (error) {
        console.error('Ошибка добавления в корзину:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    }
};

async function updateCartCount() {
    try {
        const response = await fetch('/api/carts/my_cart/', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
            credentials: 'same-origin'
        });
        
        if (response.ok) {
            const cart = await response.json();
            const count = cart.items_count || cart.items?.length || 0;
            
            document.querySelectorAll('.cart-count').forEach(el => {
                el.textContent = count;
            });
        }
    } catch (error) {
        console.error('Ошибка обновления счётчика корзины:', error);
    }
}

async function apiRequest(url, options = {}) {
    const csrfToken = getCSRFToken();
    
    const defaultOptions = {
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: 'same-origin',
    };
    const mergedOptions = { ...defaultOptions, ...options };
    if (mergedOptions.body && typeof mergedOptions.body === 'object') {
        mergedOptions.headers['Content-Type'] = 'application/json';
        mergedOptions.body = JSON.stringify(mergedOptions.body);
    }
    const response = await fetch(url, mergedOptions);
    if (response.status === 401) {
        showNotification('Необходимо войти в систему', 'error');
        setTimeout(() => window.location.href = '/login/', 1500);
        throw new Error('Unauthorized');
    }
    if (response.status === 403) {
        showNotification('Доступ запрещён', 'error');
        throw new Error('Forbidden');
    }
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}`);
    }
    return await response.json();
}