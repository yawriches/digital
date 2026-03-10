/* ==========================================
   SMART WATCHES - Main JavaScript
   ========================================== */

document.addEventListener('DOMContentLoaded', function () {

    // ---- Navbar Scroll Effect ----
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ---- Mobile Menu ----
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', function () {
            mobileMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }

    // ---- Flash Message Auto-Dismiss ----
    document.querySelectorAll('.flash-message').forEach(function (msg) {
        setTimeout(function () {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(20px)';
            setTimeout(function () { msg.remove(); }, 300);
        }, 4000);
    });

    // ---- Live Search Suggestions ----
    const searchInput = document.getElementById('searchInput');
    const suggestions = document.getElementById('searchSuggestions');
    let searchTimeout;

    if (searchInput && suggestions) {
        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            const q = this.value.trim();
            if (q.length < 2) {
                suggestions.classList.remove('active');
                suggestions.innerHTML = '';
                return;
            }
            searchTimeout = setTimeout(function () {
                fetch('/api/search-suggestions?q=' + encodeURIComponent(q))
                    .then(function (r) { return r.json(); })
                    .then(function (data) {
                        if (data.length === 0) {
                            suggestions.classList.remove('active');
                            suggestions.innerHTML = '';
                            return;
                        }
                        let html = '';
                        data.forEach(function (item) {
                            html += '<a href="/product/' + item.slug + '" class="suggestion-item">';
                            html += '<img src="' + item.image + '" alt="' + item.name + '">';
                            html += '<div class="suggestion-info">';
                            html += '<div class="suggestion-name">' + item.name + '</div>';
                            html += '<div class="suggestion-price">$' + item.price.toFixed(2) + '</div>';
                            html += '</div></a>';
                        });
                        suggestions.innerHTML = html;
                        suggestions.classList.add('active');
                    })
                    .catch(function () {
                        suggestions.classList.remove('active');
                    });
            }, 300);
        });

        document.addEventListener('click', function (e) {
            if (!e.target.closest('.search-wrapper')) {
                suggestions.classList.remove('active');
            }
        });
    }

    // ---- Quantity Selector ----
    document.querySelectorAll('.qty-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const input = this.parentElement.querySelector('.qty-input');
            let val = parseInt(input.value) || 1;
            if (this.dataset.action === 'increase') {
                val++;
            } else if (this.dataset.action === 'decrease' && val > 1) {
                val--;
            }
            input.value = val;
        });
    });

    // ---- Add to Cart AJAX ----
    document.querySelectorAll('.add-to-cart-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(this);
            const btn = this.querySelector('button[type="submit"]');
            const originalText = btn.innerHTML;
            btn.innerHTML = 'Adding...';
            btn.disabled = true;

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data.success) {
                    const badge = document.getElementById('cartBadge');
                    if (badge) badge.textContent = data.cart_count;
                    btn.innerHTML = 'Added!';
                    setTimeout(function () {
                        btn.innerHTML = originalText;
                        btn.disabled = false;
                    }, 1500);
                }
            })
            .catch(function () {
                btn.innerHTML = originalText;
                btn.disabled = false;
            });
        });
    });

    // ---- Wishlist Toggle AJAX ----
    document.querySelectorAll('.wishlist-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(this);
            const btn = this.querySelector('button');

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data.status === 'added') {
                    btn.classList.add('active');
                    btn.title = 'Remove from Wishlist';
                } else {
                    btn.classList.remove('active');
                    btn.title = 'Add to Wishlist';
                }
            })
            .catch(function () {});
        });
    });

    // ---- Product Gallery ----
    const galleryMain = document.getElementById('galleryMain');
    const galleryThumbs = document.querySelectorAll('.gallery-thumb');
    if (galleryMain && galleryThumbs.length) {
        galleryThumbs.forEach(function (thumb) {
            thumb.addEventListener('click', function () {
                galleryThumbs.forEach(function (t) { t.classList.remove('active'); });
                this.classList.add('active');
                galleryMain.src = this.dataset.src;
            });
        });
    }

    // ---- Star Rating Input ----
    const starLabels = document.querySelectorAll('.star-rating label');
    starLabels.forEach(function (label) {
        label.addEventListener('click', function () {
            const val = this.getAttribute('for').replace('star', '');
            const input = document.getElementById('ratingInput');
            if (input) input.value = val;
        });
    });

    // ---- Scroll Animations ----
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(function (el) {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // ---- Price Range Filter ----
    const priceForm = document.getElementById('priceFilterForm');
    if (priceForm) {
        priceForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const min = this.querySelector('[name="min_price"]').value;
            const max = this.querySelector('[name="max_price"]').value;
            const url = new URL(window.location.href);
            if (min) url.searchParams.set('min_price', min);
            if (max) url.searchParams.set('max_price', max);
            window.location.href = url.toString();
        });
    }

    // ---- Sort Change ----
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', function () {
            const url = new URL(window.location.href);
            url.searchParams.set('sort', this.value);
            window.location.href = url.toString();
        });
    }

});

/* ---- Admin Chart (using Canvas) ---- */
function drawRevenueChart(canvasId, labels, data) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width = canvas.parentElement.clientWidth;
    const H = canvas.height = 300;
    const padding = { top: 30, right: 30, bottom: 50, left: 70 };
    const chartW = W - padding.left - padding.right;
    const chartH = H - padding.top - padding.bottom;

    const maxVal = Math.max(...data, 1);

    ctx.clearRect(0, 0, W, H);

    // Grid lines
    ctx.strokeStyle = '#2a2a2a';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = padding.top + (chartH / 4) * i;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(W - padding.right, y);
        ctx.stroke();

        ctx.fillStyle = '#666';
        ctx.font = '11px Inter, sans-serif';
        ctx.textAlign = 'right';
        const val = maxVal - (maxVal / 4) * i;
        ctx.fillText('$' + val.toFixed(0), padding.left - 10, y + 4);
    }

    // Data line
    if (data.length > 1) {
        const stepX = chartW / (data.length - 1);

        // Gradient fill
        const gradient = ctx.createLinearGradient(0, padding.top, 0, H - padding.bottom);
        gradient.addColorStop(0, 'rgba(200, 164, 94, 0.3)');
        gradient.addColorStop(1, 'rgba(200, 164, 94, 0)');

        ctx.beginPath();
        ctx.moveTo(padding.left, padding.top + chartH - (data[0] / maxVal) * chartH);
        for (let i = 1; i < data.length; i++) {
            const x = padding.left + stepX * i;
            const y = padding.top + chartH - (data[i] / maxVal) * chartH;
            ctx.lineTo(x, y);
        }
        ctx.strokeStyle = '#c8a45e';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Fill area
        ctx.lineTo(padding.left + stepX * (data.length - 1), H - padding.bottom);
        ctx.lineTo(padding.left, H - padding.bottom);
        ctx.closePath();
        ctx.fillStyle = gradient;
        ctx.fill();

        // Dots
        for (let i = 0; i < data.length; i++) {
            const x = padding.left + stepX * i;
            const y = padding.top + chartH - (data[i] / maxVal) * chartH;
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#c8a45e';
            ctx.fill();
            ctx.strokeStyle = '#0a0a0a';
            ctx.lineWidth = 2;
            ctx.stroke();
        }

        // Labels
        ctx.fillStyle = '#666';
        ctx.font = '10px Inter, sans-serif';
        ctx.textAlign = 'center';
        for (let i = 0; i < labels.length; i++) {
            const x = padding.left + stepX * i;
            ctx.fillText(labels[i], x, H - padding.bottom + 20);
        }
    }
}

function drawStatusChart(canvasId, statusCounts) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width = canvas.parentElement.clientWidth;
    const H = canvas.height = 250;

    const statuses = Object.keys(statusCounts);
    const values = Object.values(statusCounts);
    const total = values.reduce(function (a, b) { return a + b; }, 0) || 1;

    const colors = {
        pending: '#f39c12',
        processing: '#3498db',
        shipped: '#9b59b6',
        delivered: '#27ae60',
        cancelled: '#e74c3c'
    };

    const barW = Math.min(60, (W - 100) / statuses.length - 10);
    const gap = (W - 60 - barW * statuses.length) / (statuses.length + 1);
    const maxH = H - 80;

    ctx.clearRect(0, 0, W, H);

    const maxVal = Math.max(...values, 1);

    statuses.forEach(function (status, i) {
        const x = 30 + gap * (i + 1) + barW * i;
        const h = (values[i] / maxVal) * maxH;
        const y = H - 40 - h;

        ctx.fillStyle = colors[status] || '#666';
        ctx.beginPath();
        ctx.roundRect(x, y, barW, h, 4);
        ctx.fill();

        ctx.fillStyle = '#a0a0a0';
        ctx.font = '10px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(status.charAt(0).toUpperCase() + status.slice(1), x + barW / 2, H - 20);

        ctx.fillStyle = '#f0f0f0';
        ctx.font = '12px Inter, sans-serif';
        ctx.fillText(values[i], x + barW / 2, y - 8);
    });
}
