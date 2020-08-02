document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#follow-button").addEventListener("click", (event) => {
        user = document.querySelector("#follow-button").getAttribute("data-user");
        action = document.querySelector("#follow-button").textContent.trim();

        fetch("/follow", {
            method: "POST",
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            body: JSON.stringify({
                user: user,
                action: action
            })
          })
            .then(response => response.json())
            .then(result => {
              console.log(result);
              if (result.status == 201) {
                document.querySelector("#follow-button").textContent = `${result.action}`;
                document.querySelector("#follower-p").textContent = `Followers: ${result.followers}`;
              } else {
                  alert(`${result.message}`);
              }
            
            });
    });

    document.querySelector(".edit").array.forEach(element => {
        element.addEventListener("click", (event) => {
            postId = element.getAttribute("data-post_id");
            edit = document.querySelector(`#edit-${postId}`);

            action = edit.innerHTML;

            if (action == "Edit") {
                edit.innerHTML = "Save"

                document.querySelector(`#edit-${postId}`).style.display = "none";
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
