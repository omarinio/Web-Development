// Document Content load listener 
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // document.querySelector('form').addEventListener('submit', () => send_email(event));

  // By default, load the inbox
  load_mailbox('inbox');
});

// Compose Email function
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('form').onsubmit = () => {
    event.preventDefault();
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
  
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        load_mailbox('sent');
        return false;
    });
    
  }
    
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      for (email in emails) {
        var email_div = document.createElement('div');
        email_div.style.border = 'solid black 2px';
        email_div.style.height = '50px';

        var sender_p = document.createElement('div');
        var subject_p = document.createElement('div');
        var timestamp_p = document.createElement('div');

        sender_p.innerHTML = emails[email].sender;
        subject_p.innerHTML = emails[email].subject;
        timestamp_p.innerHTML = emails[email].timestamp;

        sender_p.setAttribute("style", "font-weight: bold; float: left; position: relative; top: 50%; transform: translateY(-50%); padding-left: 4px");
        subject_p.setAttribute("style", "float: left; padding-left: 10px; position: relative; top: 50%; transform: translateY(-50%)");
        timestamp_p.setAttribute("style", "float: right; padding-right: 4px; position: relative; top: 50%; transform: translateY(-50%); color: grey");

        email_div.appendChild(sender_p);
        email_div.appendChild(subject_p);
        email_div.appendChild(timestamp_p);
      

        if (emails[email].read == true && mailbox == 'inbox') {
          email_div.style.backgroundColor = 'lightgrey';
        }

        document.querySelector("#emails-view").appendChild(email_div);
        
      }
  });
}