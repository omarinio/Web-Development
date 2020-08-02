document.addEventListener('DOMContentLoaded', function() {

    //edit post event
    document.querySelectorAll(".edit-link").forEach((element) => {
        element.addEventListener("click", (event) => {
            event.preventDefault();
            postId = element.getAttribute("data-post_id");
            edit = document.querySelector(`#edit-${postId}`);

            action = edit.innerHTML;

            //if edit
            if (action == "Edit") {
                edit.innerHTML = "Save";
                document.querySelector(`#edit-div-${postId}`).style.display = "block";
                document.querySelector(`#content-${postId}`).style.display = "none";
            //if save
            } else {
                fetch("/edit", {
                    method: "PUT",
                    headers: { "X-CSRFToken": getCookie('csrftoken') },
                    body: JSON.stringify({
                        post_id: postId,
                        post: document.querySelector(`#text-${postId}`).value
                    })
                })
                .then(response => {
                    console.log(response.json());
                    document.querySelector(`#edit-div-${postId}`).style.display = "none";
                    document.querySelector(`#content-${postId}`).style.display = "block";
                    edit.innerHTML = "Edit";
                    document.querySelector(`#content-${postId}`).innerHTML = document.querySelector(`#text-${postId}`).value;
                })
                .catch(e => console.log(e));
                
            }
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
