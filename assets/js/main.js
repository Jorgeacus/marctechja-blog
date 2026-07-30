document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav-links');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('active');
    });
    document.addEventListener('click', (e) => {
      if (!toggle.contains(e.target) && !nav.contains(e.target)) {
        nav.classList.remove('active');
      }
    });
  }

  const params = new URLSearchParams(window.location.search);
  if (params.get('subscribed') === 'true') {
    const msg = document.getElementById('subscribe-msg');
    if (msg) {
      msg.style.display = 'block';
      setTimeout(() => { msg.style.display = 'none'; }, 8000);
    }
  }

  if (window.location.hash) {
    setTimeout(() => {
      const el = document.querySelector(window.location.hash);
      if (el) {
        const offset = 90;
        const top = el.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    }, 100);
  }

  const subForm = document.getElementById('subscribe-form');
  const subFeedback = document.getElementById('subscribe-feedback');
  if (subForm && subFeedback) {
    subForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      subFeedback.style.display = 'none';
      const formData = new URLSearchParams(new FormData(subForm));
      try {
        const res = await fetch('SUBSTITUIR_PELO_URL_DO_APPS_SCRIPT', {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        if (data.success) {
          subFeedback.textContent = '✅ Subscrição confirmada! Vais começar a receber as notificações diárias.';
          subFeedback.style.display = 'block';
          subForm.reset();
        } else {
          subFeedback.textContent = '❌ Erro ao subscrever. Tenta novamente mais tarde.';
          subFeedback.style.display = 'block';
        }
      } catch (err) {
        subFeedback.textContent = '❌ Erro de conexão. Tenta novamente mais tarde.';
        subFeedback.style.display = 'block';
      }
    });
  }
});
