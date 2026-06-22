document.addEventListener('DOMContentLoaded', () => {
    const profileForm = document.getElementById('profile-form');
    if (!profileForm) return;

    loadProfile();
    loadOrders();

    profileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            full_name: document.getElementById('full_name').value,
            phone: document.getElementById('phone').value,
            address: document.getElementById('address').value,
        };
        await apiRequest('/api/me/', { method: 'PATCH', body: data });
        showNotification('Профиль обновлён', 'success');
    });
});

async function loadProfile() {
    try {
        const data = await apiRequest('/api/me/');
        document.getElementById('username').value = data.username || '';
        document.getElementById('email').value = data.email || '';
        document.getElementById('full_name').value = data.full_name || '';
        document.getElementById('phone').value = data.phone || '';
        document.getElementById('address').value = data.address || '';
        document.getElementById('role').value = data.role || '';
    } catch (err) {
        showNotification('Не удалось загрузить профиль', 'error');
    }
}

async function loadOrders() {
    const container = document.getElementById('orders-container');
    try {
        const data = await apiRequest('/api/orders/');
        const orders = data.results || data;
        if (orders.length === 0) {
            container.innerHTML = '<p class="text-muted">У вас пока нет заказов</p>';
            return;
        }
        let html = '<table class="table table-sm"><thead><tr><th>№</th><th>Дата</th><th>Сумма</th><th></th></tr></thead><tbody>';
        orders.forEach(o => {
            html += `<tr>
                <td>#${o.id}</td>
                <td>${new Date(o.created_at).toLocaleDateString('ru-RU')}</td>
                <td>${o.total_cost} руб.</td>
                <td><button class="btn btn-sm btn-primary" onclick="showOrderDetail(${o.id})">Подробнее</button></td>
            </tr>`;
        });
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (err) {
        container.innerHTML = '<p class="text-danger">Ошибка загрузки заказов</p>';
    }
}

async function showOrderDetail(id) {
    try {
        const order = await apiRequest(`/api/orders/${id}/`);
        let html = `<h6>Заказ #${order.id}</h6><p>Адрес: ${order.delivery_address}</p><ul>`;
        order.items.forEach(item => {
            html += `<li>${item.product_name} — ${item.quantity} шт. × ${item.price} руб.</li>`;
        });
        html += `</ul><p><strong>Итого: ${order.total_cost} руб.</strong></p>`;
        document.getElementById('orders-container').innerHTML = html;
    } catch (err) {
        showNotification('Не удалось загрузить заказ', 'error');
    }
}