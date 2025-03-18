/**
 * Ulimi Wise - Marketplace JavaScript
 * Handles marketplace functionality like filtering, adding, editing products
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Marketplace script loaded');
    
    // Initialize product filters
    initProductFilters();
    
    // Initialize product form
    initProductForm();
    
    // Initialize edit product buttons
    initEditProductButtons();
    
    // Initialize delete product buttons
    initDeleteProductButtons();
});

/**
 * Initialize product filters
 */
function initProductFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const priceFilter = document.getElementById('priceFilter');
    const searchInput = document.getElementById('searchProduct');
    
    // Apply filters when changed
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterProducts);
    }
    
    if (priceFilter) {
        priceFilter.addEventListener('change', filterProducts);
    }
    
    if (searchInput) {
        searchInput.addEventListener('input', filterProducts);
    }
}

/**
 * Filter products based on selected filters
 */
function filterProducts() {
    const categoryFilter = document.getElementById('categoryFilter');
    const priceFilter = document.getElementById('priceFilter');
    const searchInput = document.getElementById('searchProduct');
    
    const selectedCategory = categoryFilter ? categoryFilter.value : '';
    const selectedPrice = priceFilter ? priceFilter.value : '';
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        const category = card.dataset.category;
        const price = parseFloat(card.dataset.price);
        const productName = card.querySelector('.card-title').textContent.toLowerCase();
        const description = card.querySelector('.card-text').textContent.toLowerCase();
        
        let showCard = true;
        
        // Apply category filter
        if (selectedCategory && category !== selectedCategory) {
            showCard = false;
        }
        
        // Apply price filter
        if (selectedPrice) {
            switch (selectedPrice) {
                case 'under25':
                    if (price >= 25) showCard = false;
                    break;
                case '25to50':
                    if (price < 25 || price > 50) showCard = false;
                    break;
                case '50to100':
                    if (price < 50 || price > 100) showCard = false;
                    break;
                case 'over100':
                    if (price <= 100) showCard = false;
                    break;
            }
        }
        
        // Apply search filter
        if (searchTerm && !productName.includes(searchTerm) && !description.includes(searchTerm)) {
            showCard = false;
        }
        
        // Show or hide the card
        if (showCard) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
    
    // Update the count of visible products
    updateProductCount();
}

/**
 * Update the count of visible products
 */
function updateProductCount() {
    const visibleProducts = document.querySelectorAll('.product-card:not([style*="display: none"])').length;
    const totalProducts = document.querySelectorAll('.product-card').length;
    
    const countElement = document.getElementById('productCount');
    if (countElement) {
        countElement.textContent = `${visibleProducts} of ${totalProducts} products`;
    }
    
    // Show no results message if needed
    const noResultsElement = document.getElementById('noResults');
    if (noResultsElement) {
        if (visibleProducts === 0) {
            noResultsElement.style.display = 'block';
        } else {
            noResultsElement.style.display = 'none';
        }
    }
}

/**
 * Initialize the product form
 */
function initProductForm() {
    const addProductForm = document.getElementById('addProductForm');
    
    if (addProductForm) {
        addProductForm.addEventListener('submit', function(e) {
            const nameInput = document.getElementById('productName');
            const priceInput = document.getElementById('productPrice');
            const quantityInput = document.getElementById('productQuantity');
            const unitInput = document.getElementById('productUnit');
            const categoryInput = document.getElementById('productCategory');
            
            // Validate required fields
            let isValid = true;
            
            if (!nameInput.value.trim()) {
                isValid = false;
                nameInput.classList.add('is-invalid');
            } else {
                nameInput.classList.remove('is-invalid');
            }
            
            if (!priceInput.value.trim() || isNaN(parseFloat(priceInput.value))) {
                isValid = false;
                priceInput.classList.add('is-invalid');
            } else {
                priceInput.classList.remove('is-invalid');
            }
            
            if (!quantityInput.value.trim() || isNaN(parseFloat(quantityInput.value))) {
                isValid = false;
                quantityInput.classList.add('is-invalid');
            } else {
                quantityInput.classList.remove('is-invalid');
            }
            
            if (!unitInput.value.trim()) {
                isValid = false;
                unitInput.classList.add('is-invalid');
            } else {
                unitInput.classList.remove('is-invalid');
            }
            
            if (!categoryInput.value.trim()) {
                isValid = false;
                categoryInput.classList.add('is-invalid');
            } else {
                categoryInput.classList.remove('is-invalid');
            }
            
            // Prevent form submission if validation fails
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields correctly.', 'danger');
            }
        });
    }
}

/**
 * Initialize edit product buttons
 */
function initEditProductButtons() {
    const editButtons = document.querySelectorAll('.edit-product-btn');
    
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const productData = JSON.parse(this.dataset.product);
            
            // Populate the edit form
            document.getElementById('editProductId').value = productId;
            document.getElementById('editProductName').value = productData.name;
            document.getElementById('editProductDescription').value = productData.description || '';
            document.getElementById('editProductPrice').value = productData.price;
            document.getElementById('editProductQuantity').value = productData.quantity;
            document.getElementById('editProductUnit').value = productData.unit;
            document.getElementById('editProductCategory').value = productData.category;
            document.getElementById('editProductAvailable').checked = productData.is_available;
            
            // Show the modal
            const editModal = new bootstrap.Modal(document.getElementById('editProductModal'));
            editModal.show();
        });
    });
}

/**
 * Initialize delete product buttons
 */
function initDeleteProductButtons() {
    const deleteButtons = document.querySelectorAll('.delete-product-btn');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const productName = this.dataset.productName;
            
            // Set the product ID and name in the confirmation modal
            document.getElementById('deleteProductId').value = productId;
            document.getElementById('productNameToDelete').textContent = productName;
            
            // Show the modal
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteProductModal'));
            deleteModal.show();
        });
    });
}

/**
 * Create a product card element
 * @param {Object} product - Product data
 * @returns {HTMLElement} - Product card element
 */
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'col-12 col-md-6 col-lg-4 mb-4';
    card.innerHTML = `
        <div class="card h-100 product-card shadow-sm" data-category="${product.category}" data-price="${product.price}">
            <div class="card-header bg-light">
                <h5 class="card-title mb-0">${product.name}</h5>
            </div>
            <div class="card-body">
                <p class="card-text">${product.description || 'No description provided.'}</p>
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge bg-primary">${product.category}</span>
                    <h5 class="text-primary mb-0">${formatCurrency(product.price)}</h5>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <span><strong>Quantity:</strong> ${product.quantity} ${product.unit}</span>
                    <span><strong>Seller:</strong> ${product.seller_username}</span>
                </div>
            </div>
            <div class="card-footer d-flex justify-content-between">
                <span class="text-muted small">Posted: ${formatDate(product.created_at)}</span>
                <div>
                    <button class="btn btn-sm btn-outline-primary contact-seller-btn" data-seller-id="${product.seller_id}">Contact</button>
                </div>
            </div>
        </div>
    `;
    
    // Add contact seller functionality
    const contactBtn = card.querySelector('.contact-seller-btn');
    contactBtn.addEventListener('click', function() {
        const sellerId = this.dataset.sellerId;
        // Redirect to chatbot with seller info
        window.location.href = `/chatbot?seller_id=${sellerId}`;
    });
    
    return card;
}
