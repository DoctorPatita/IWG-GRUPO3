function like_post(blog_id, likeButton) {
    console.log('Like button clicked for blog_id:', blog_id);

    $.ajax({
        url: '/blog/like_post/' + blog_id + '/',
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            var likesCount = document.getElementById('likesCount' + blog_id);
            likesCount.innerText = data.likes_count;

            // Togglea la clase "liked" en el botón
            likeButton.classList.toggle('liked');
        },
        error: function(error) {
            console.error('Error al enviar la solicitud:', error);
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    var likeButtons = document.querySelectorAll('.btn-like');

    likeButtons.forEach(function(likeButton) {
        likeButton.addEventListener('click', function() {
            var blog_id = this.getAttribute('data-blog-id');

            // Llama a la función para manejar el like/deslike
            like_post(blog_id, this);
        });
    });
});