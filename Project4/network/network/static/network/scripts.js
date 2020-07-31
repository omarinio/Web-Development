document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#follow-button").addEventListener("click", (event) => {
        user = document.querySelector("#follow-button").getAttribute("data-user");
        action = document.querySelector("#follow-button").textContent.trim();

        fetch("/follow", {
            method: "POST",
            // headers: { "X-CSRFToken": getCookie('csrftoken') },
            body: JSON.stringify({
                user: user,
                action: action
            })
          })
            .then(response => response.json())
            .then(result => {
              console.log(result);

              document.querySelector("#follow-button").textContent = `${result.action}`;
              document.querySelector("#follower-p").textContent = `Followers: ${result.followers}`
            });
    });

    // document.querySelector("#newpost").onsubmit = (event) => {
    //     event.preventDefault()
    //     var body = document.querySelector("#compose-post").value;

    //     fetch('/new_post', {
    //         method: 'POST',
    //         // headers: { "X-CSRFToken": getCookie('csrftoken') },
    //         body: JSON.stringify({
    //             body: body
    //         })
    //     })
    //     .then(result => {
    //         if ('error' in result) {
    //             console.log(result);
    //             var alert_div = document.createElement('div');
    //             alert_div.setAttribute("class", "alert alert-danger alert-dismissible");
    //             alert_div.setAttribute("role", "alert");
    //             alert_div.innerHTML = "Post cannot be empty";
    //             document.querySelector('#newpost').insertBefore(alert_div, document.querySelector('#newpost').firstChild);
    //             return false;
    //         } else {
    //             console.log(result);
    //         }
    //     });

    //     // if (body === '') {
    //     //     var alert_div = document.createElement('div');
    //     //     alert_div.setAttribute("class", "alert alert-danger alert-dismissible");
    //     //     alert_div.setAttribute("role", "alert");
    //     //     alert_div.innerHTML = "Post cannot be empty";
    //     //     document.querySelector('#newpost').insertBefore(alert_div, document.querySelector('#newpost').firstChild);
    //     // }
    // }


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
