document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('n'));


  document.getElementById('Status').style.display ='none';


  //submit
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(arg) {
  document.getElementById('Status').style.display ='none';
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#one-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if (arg == 'n') {
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {
    fetch(`/emails/${arg}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#compose-recipients').value = email.sender;
      let subject = email.subject;
      if (subject.startsWith ('Re:')) {
        document.querySelector('#compose-subject').value = subject;
      } else {
        document.querySelector('#compose-subject').value = `Re:${subject}`;
      }
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n\n${email.body}`;

    });
    
    
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  if (mailbox == 'sent'){
    document.getElementById('Status').style.display ='block';
  } else {
    document.getElementById('Status').style.display ='none';
  }
 
  document.querySelector('#one-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show all emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      Array.from(emails).forEach((one_email) => {
        const element = document.createElement('div');
        element.className = 'list-of-emails';
        
        if (one_email.read == false) {
          element.style.backgroundColor = 'white';
        } else { 
          element.style.backgroundColor = 'grey';
        };

        element.innerHTML = `<p>From: ${one_email.sender}</p> <p><i>${one_email.subject}</i></p> <p>sent at ${one_email.timestamp}</p>`;
        document.querySelector('#emails-view').append(element);

        element.addEventListener('click', function() {
          open_email(one_email.id, mailbox)
        });
        document.querySelector('#emails-view').style.display = 'block';
      });
  });


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


}


function send_email(event){
  event.preventDefault();
   //Post data
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result

      // it doesnt see div element inside 
      document.getElementById('Status').style.display ='block';
      let element = document.getElementById('Status');
      if ('error' in result) {
        element.style.color = 'red'
        result = JSON.stringify(result['error']).replace('"','');
        element.innerHTML = result.replace('"','');
        
      } else {
        element.style.color = 'blue'
        result = JSON.stringify(result['message']).replace('"','');
        element.innerHTML = result.replace('"','');
        
      }
      console.log(result);
      load_mailbox('sent');
  });
  
}

function open_email(id, mailbox) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#one-email-view').style.display = 'block';
  
  

  if (mailbox == 'inbox'){
    document.querySelector('#unarchive').style.display = 'none';
    document.querySelector('#archive').style.display = 'block';
    document.querySelector('#archive').addEventListener('click', () => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
      .then(() => {load_mailbox('inbox')})
    });
    
  } else if (mailbox == 'archive') {
    document.querySelector('#unarchive').style.display = 'block';
    document.querySelector('#archive').style.display = 'none';
    document.querySelector('#unarchive').addEventListener('click', function() {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
      .then(() => {load_mailbox('inbox')})
    });
    
  } else {
    document.querySelector('#unarchive').style.display = 'none';
    document.querySelector('#archive').style.display = 'none';
  };

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#header').innerHTML = `
      <b>From:</b> ${email.sender}<br>
      <b>To:</b> ${email.recipients}<br>
      <b>Subject:</b> ${email.subject}<br>
      <b>Timestamp:</b> ${email.timestamp}
    `;

    document.querySelector('#bodytext').innerHTML = email.body;

    
    console.log(email)

    //reply to email
    if (mailbox == 'sent' || mailbox == 'archive') {
      document.querySelector('#replydiv').style.display ='none';
    } else {
      document.querySelector('#replydiv').style.display ='block';
      document.querySelector('#reply').addEventListener('click', () => compose_email(id));
    }

  });


  
 
}
