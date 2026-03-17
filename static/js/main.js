// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// Auto-dismiss messages after 5s
document.querySelectorAll('.message').forEach(el => {
  setTimeout(() => { el.style.transition = 'opacity .5s'; el.style.opacity = '0'; setTimeout(() => el.remove(), 500); }, 5000);
});

// CPF mask
function maskCPF(input) {
  let v = input.value.replace(/\D/g, '').substring(0, 11);
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  input.value = v;
}

// Phone mask
function maskPhone(input) {
  let v = input.value.replace(/\D/g, '').substring(0, 11);
  v = v.replace(/^(\d{2})(\d)/, '($1) $2');
  v = v.replace(/(\d{5})(\d)/, '$1-$2');
  input.value = v;
}

// Apply masks to forms
document.addEventListener('DOMContentLoaded', () => {
  const cpfField = document.querySelector('input[name="cpf"]');
  if (cpfField) cpfField.addEventListener('input', () => maskCPF(cpfField));

  const telField = document.querySelector('input[name="telefone"]');
  if (telField) telField.addEventListener('input', () => maskPhone(telField));

  // Set min date on date fields to tomorrow
  const dateFields = document.querySelectorAll('input[type="date"]');
  dateFields.forEach(field => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    field.min = tomorrow.toISOString().split('T')[0];
  });
});
