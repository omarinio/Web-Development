document.addEventListener('DOMContentLoaded', function() {

    //edit post event
    document.querySelectorAll(".like-button").forEach((element) => {
        element.addEventListener("click", (event) => {
            event.preventDefault();
            postId = element.getAttribute("data-post_id");
            action = element.getAttribute(`data-action`);


            fetch("/like", {
                method: "PUT",
                headers: { "X-CSRFToken": getCookie('csrftoken') },
                body: JSON.stringify({
                    post_id: postId,
                    action: action
                })
            })
            .then(response => response.json())
            .then(response => {
                if (response.status == 201) {
                    console.log(response);
                    var likes = parseInt(document.querySelector(`#like-count-${postId}`).innerHTML);
                    if (action === "like") {
                        document.querySelector(`#liked-${postId}`).style.display = "block";
                        document.querySelector(`#unliked-${postId}`).style.display = "none";
                        document.querySelector(`#like-count-${postId}`).innerHTML = likes + 1;
                    } else {
                        document.querySelector(`#liked-${postId}`).style.display = "none";
                        document.querySelector(`#unliked-${postId}`).style.display = "block";
                        document.querySelector(`#like-count-${postId}`).innerHTML = likes - 1;
                    }
                } else {    
                    alert(`${response.message}`);
                }
            })
            .catch(e => console.log(e));
                
        });
    });


});

// The following function are copying from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
