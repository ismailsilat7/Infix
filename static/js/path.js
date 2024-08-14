function selectPath() {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/selectpath';
  document.body.appendChild(form);
  form.submit();
}