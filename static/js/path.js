function selectPathO() {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/selectpathoauth';

  const input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'selected_path';
  input.value = 'O Level';

  const pathIdInput = document.createElement('input');
  pathIdInput.type = 'hidden';
  pathIdInput.name = 'path_id';
  pathIdInput.value = '1';  

  form.appendChild(input);
  form.appendChild(pathIdInput);
  document.body.appendChild(form);
  form.submit();
}
function selectPathA() {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/selectpathoauth';
  const input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'selected_path';
  input.value = 'A Level';

  const pathIdInput = document.createElement('input');
  pathIdInput.type = 'hidden';
  pathIdInput.name = 'path_id';
  pathIdInput.value = '2';

  form.appendChild(input);
  form.appendChild(pathIdInput);
  document.body.appendChild(form);
  form.submit();
}