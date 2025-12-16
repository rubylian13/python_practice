document.querySelectorAll('.product-item').forEach(item => {
    item.addEventListener('click', function () {

        const productId = this.getAttribute('data-id');

        fetch('/add_to_cart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message); // 加入成功提示
            updateCartCount();   // 更新右上角購物車 badge
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.querySelector('table tbody');

    // 更新購物車右上角 badge
    function updateCartCount(count) {
        fetch('/cart_count')
            .then(res => res.json())
            .then(data => {
                const badge = document.getElementById('cart-badge');
                badge.textContent = data.count;
                badge.style.display = data.count > 0 ? 'inline-block' : 'none';
            });
    }

    // 更新 subtotal 和 total
    function updateCartTotals() {
        const rows = tbody.querySelectorAll('tr');
        let subtotal = 0;

        rows.forEach(tr => {
            const price = parseFloat(tr.querySelector('td:nth-child(3)').textContent.replace('$','').trim());
            const qty = parseInt(tr.querySelector('.quantity-amount').value);
            const totalCell = tr.querySelector('td:nth-child(5)');
            totalCell.textContent = `$ ${(price * qty).toFixed(2)}`;
            subtotal += price * qty;
        });

        const tax = 0; // 可加運費或稅金
        const total = subtotal + tax;

        document.getElementById('cart-subtotal').textContent = `$ ${subtotal.toFixed(2)}`;
        document.getElementById('cart-total').textContent = `$ ${total.toFixed(2)}`;
    }

    // 載入購物車
    function loadCart() {
        fetch('/cart_data')
            .then(res => res.json())
            .then(cart => {
                tbody.innerHTML = ''; // 清空舊資料

                cart.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.setAttribute('data-id', item.id);
                    tr.innerHTML = `
                        <td class="product-thumbnail">
                            <img src="./static/images/${item.image}" alt="Image" class="img-fluid">
                        </td>
                        <td class="product-name">
                            <h2 class="h5 text-black">${item.name}</h2>
                        </td>
                        <td>$ ${item.price.toFixed(2)}</td>
                        <td>
                            <div class="input-group mb-3 d-flex align-items-center quantity-container" style="max-width: 120px;">
                                <button class="btn btn-outline-black decrease" type="button">&minus;</button>
                                <input type="text" class="form-control text-center quantity-amount" value="${item.qty}">
                                <button class="btn btn-outline-black increase" type="button">&plus;</button>
                            </div>
                        </td>
                        <td>$ ${(item.price * item.qty).toFixed(2)}</td>
                        <td>
                            <button class="btn btn-black btn-sm remove-item">X</button>
                        </td>
                    `;
                    tbody.appendChild(tr);

                    // 刪除商品
                    tr.querySelector('.remove-item').addEventListener('click', (e) => {
                        e.preventDefault();
                        fetch('/cart/remove_from_cart', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ product_id: item.id })
                        })
                        .then(res => res.json())
                        .then(data => {
                            tr.remove();
                            updateCartCount(data.count);
                            updateCartTotals();
                        });
                    });

                    // 增加數量
                    tr.querySelector('.increase').addEventListener('click', () => {
                        let input = tr.querySelector('.quantity-amount');
                        input.value = parseInt(input.value) + 1;
                        updateQuantity(item.id, parseInt(input.value));
                    });

                    // 減少數量
                    tr.querySelector('.decrease').addEventListener('click', () => {
                        let input = tr.querySelector('.quantity-amount');
                        let qty = parseInt(input.value);
                        if (qty > 1) {
                            input.value = qty - 1;
                            updateQuantity(item.id, parseInt(input.value));
                        }
                    });

                    // 手動輸入數量
                    tr.querySelector('.quantity-amount').addEventListener('change', () => {
                        let input = tr.querySelector('.quantity-amount');
                        let qty = parseInt(input.value);
                        if (isNaN(qty) || qty < 1) qty = 1;
                        input.value = qty;
                        updateQuantity(item.id, qty);
                    });

                });

                updateCartTotals(); // 載入完就更新總額
            });
    }

    // 更新後端數量
    function updateQuantity(product_id, qty) {
        fetch('/cart/update_quantity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: product_id, quantity: qty })
        })
        .then(res => res.json())
        .then(data => {
            updateCartCount(data.count);
            updateCartTotals();
        });
    }

    // 初始化
    loadCart();
});


document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('checkout-tbody');

    function loadCart() {
        fetch('/cart_data')
            .then(res => res.json())
            .then(cart => {
                tbody.innerHTML = ''; // 清空舊資料

                let subtotal = 0;

                cart.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${item.name} <strong class="mx-2">x</strong> ${item.qty}</td>
                        <td>$ ${(item.price * item.qty).toFixed(2)}</td>
                    `;
                    tbody.appendChild(tr);

                    subtotal += item.price * item.qty;
                });

                // 更新 subtotal / total，如果 HTML 有對應元素
                const subtotalEl = document.getElementById('cart-subtotal');
                const totalEl = document.getElementById('cart-total');

                if (subtotalEl) subtotalEl.textContent = `$ ${subtotal.toFixed(2)}`;
                if (totalEl) totalEl.textContent = `$ ${subtotal.toFixed(2)}`; // 如果沒稅或運費
            });
    }

    loadCart();
});

