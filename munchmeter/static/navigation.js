$(document).ready(function () {
    function loadContent(url) {
        $.ajax({
            url: url,
            method: 'GET',
            success: function (data) {
                var newContent = $(data).find('.container').html();
                $('.container').html(newContent);

                // Update the browser's URL
                history.pushState(null, '', url);

                // Re-bind internal link click handlers to the new content
                bindInternalLinks();
            },
            error: function () {
                alert('An error occurred while loading the content.');
            }
        });
    }

    function bindInternalLinks() {
        $('a.internal-link').off('click').on('click', function (e) {
            e.preventDefault();
            var url = $(this).attr('href');
            loadContent(url);
        });
    }

    // Bind internal link click handlers initially
    bindInternalLinks();

    // Handle browser's back and forward buttons
    window.onpopstate = function () {
        location.reload();
    };
});
