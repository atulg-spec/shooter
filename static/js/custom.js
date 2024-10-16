// Using ipify to fetch the public IP address
fetch('https://api.ipify.org?format=json')
  .then(response => response.json())
  .then(data => {
    console.log('Your IP address is:', data.ip);
    
    // Set the fetched IP address in the hidden input field
    const ipField = document.getElementById('id_ip_address');
    if (ipField) {
      ipField.value = data.ip;
    }
  })
  .catch(error => console.error('Error fetching the IP address:', error));
