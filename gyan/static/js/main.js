document.addEventListener('DOMContentLoaded', function () {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
        lucide.createIcons();
    }

    const messageForm = document.getElementById('message-form');
    if (messageForm) {
        messageForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(this);

            fetch('/send_message', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while sending the message.');
                });
        });
    }

    const wishlistBtn = document.getElementById('wishlist-btn');
    if (wishlistBtn) {
        wishlistBtn.addEventListener('click', function () {
            const bookId = this.getAttribute('data-book-id');
            const btn = this;

            fetch(`/wishlist/add/${bookId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        btn.innerHTML = '<i data-lucide="heart" class="w-4 h-4 inline mr-2"></i> Added to Wishlist';
                        btn.classList.add('opacity-50');
                        btn.disabled = true;
                        if (window.lucide && typeof window.lucide.createIcons === 'function') {
                            lucide.createIcons();
                        }
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred.');
                });
        });
    }

    const bookImageInput = document.getElementById('book_image');
    if (bookImageInput) {
        bookImageInput.addEventListener('change', function (e) {
            if (e.target.files.length > 0) {
                const fileName = e.target.files[0].name;
                const parent = e.target.parentElement;
                parent.innerHTML = `<i data-lucide="check-circle" class="w-8 h-8 text-accent mx-auto mb-2"></i><p class="text-sm text-accent font-bold">✓ ${fileName}</p>`;
                if (window.lucide && typeof window.lucide.createIcons === 'function') {
                    lucide.createIcons();
                }
            }
        });
    }
});

function removeFromWishlist(bookId, event) {
    event.preventDefault();
    event.stopPropagation();

    fetch(`/wishlist/remove/${bookId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                location.reload();
            }
        });
}
