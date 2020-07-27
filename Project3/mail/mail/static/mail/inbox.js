// Document Content load listener 
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

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
        // var alert_div = docuement.createElement('div');
        // alert_div.setAttribute("class", "alert alert-warning alert-dismissible fade show");
        // $('.alert').alert();
        // document.querySelector('#emails-view').appendChild(alert_div);
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
      console.log(mailbox);

      for (email in emails) {
        var email_div = document.createElement('div');
        email_div.style.border = 'solid black 2px';
        email_div.style.height = '50px';

        email_id = emails[email].id;
        mailbox_id = mailbox;
        
        email_div.setAttribute("onclick", `load_email(${email_id}, mailbox_id)`);

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

function load_email(email_id, mailbox) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#email-view').innerHTML = '';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
      console.log(mailbox);

      var email_div = document.createElement('div');
      var from_div = document.createElement('div');
      var to_div = document.createElement('div');
      var subject_div = document.createElement('div');
      var timestamp_div = document.createElement('div');
      var body_div = document.createElement('div');

      if (mailbox !== 'sent') {
        var archivebtn = document.createElement('button');
        archivebtn.setAttribute("class", 'btn btn-warning');
        if (email.archived === true) {
          archivebtn.innerHTML = 'Unarchive';
        } else {
          archivebtn.innerHTML = 'Archive';
        }
        archivebtn.setAttribute("onclick", `archive_button(${email_id}, ${email.archived})`);
        archivebtn.style.float = 'right';
        email_div.appendChild(archivebtn);
      }

      from_div.innerHTML = `<strong> From: </strong> ${email.sender}`;
      to_div.innerHTML = `<strong> To: </strong> ${email.recipients}`;
      subject_div.innerHTML = `<strong> Subject: </strong> ${email.subject}`;
      timestamp_div.innerHTML = `<strong> Date </strong> ${email.timestamp}`;
      body_div.innerHTML = email.body;

      body_div.style.paddingTop = '50px';

      email_div.appendChild(from_div);
      email_div.appendChild(to_div);
      email_div.appendChild(subject_div);
      email_div.appendChild(timestamp_div);
      email_div.appendChild(body_div);
      

      document.querySelector("#email-view").appendChild(email_div);
        
  });

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function archive_button(email_id, archive_status) {
  console.log(archive_status);

  if (archive_status === true) {
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    .then(email => {
      console.log(email);
      load_mailbox('archive');
    });

  } else {
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
    .then(email => {
      console.log(email);
      load_mailbox('inbox');
    });
  }
}