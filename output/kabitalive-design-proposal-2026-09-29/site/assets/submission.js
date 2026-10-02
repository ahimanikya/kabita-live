const button = document.querySelector('#copy-editor-address');
button?.addEventListener('click', async () => {
  const status = document.querySelector('#copy-address-status');
  const address = document.querySelector('.submission-address').textContent.trim();
  try {
    await navigator.clipboard.writeText(address);
    status.textContent = 'Email address copied.';
  } catch {
    status.textContent = 'Please select and copy the email address above.';
  }
});
