function showToast(message, type = "is-info", duration = 2000) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `notification ${type}`;
    toast.style.marginTop = "0.5rem";
    toast.innerText = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, duration);
}



document.addEventListener('click', function (e) {
    const a = e.target.closest('a.rich-link');
    if (!a) return;

    e.preventDefault(); // stop normal navigation temporarily

    const linkId = a.dataset.linkId;
    const href = a.href;
    const clickCountSpan = document.querySelector(`.click-count[data-link-id='${linkId}']`);
    if (!linkId || !href || !clickCountSpan) {
        window.open(href, '_blank'); // fallback
        return;
    }

    // Send POST request to increment click
    fetch("/forum/link/" + linkId + "/click/", {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
    }).then(res => res.json())
        .then(data => {
            if (data.success) {
                clickCountSpan.textContent = data.clicks;
            }
            // Navigate to the link after updating clicks
            window.open(href, '_blank');
        }).catch(() => {
            // fallback if something goes wrong
            window.open(href, '_blank');
        });
});