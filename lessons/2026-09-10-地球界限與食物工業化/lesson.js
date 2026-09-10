(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const notes = document.querySelector('#notes-panel');
  const toc = document.querySelector('#toc');
  let current = 0;
  const fromHash = () => Math.max(0, Math.min(slides.length - 1, Number(location.hash.match(/^#slide-(\d+)$/)?.[1] || 1) - 1));
  function show(index, hash = true) {
    current = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach((s, i) => { s.classList.toggle('active', i === current); s.setAttribute('aria-hidden', String(i !== current)); });
    document.querySelector('#counter').textContent = `${current + 1} / ${slides.length}`;
    document.querySelector('#prev').disabled = current === 0;
    document.querySelector('#next').disabled = current === slides.length - 1;
    document.querySelector('#notes-copy').textContent = slides[current].querySelector('.speaker-notes').textContent;
    if (hash) history.replaceState(null, '', `#slide-${current + 1}`);
  }
  const scale = () => document.documentElement.style.setProperty('--scale', Math.min(innerWidth / 1280, innerHeight / 720));
  const toggleNotes = () => { notes.hidden = !notes.hidden; };
  const fullscreen = async () => { try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); } catch { /* Browser may require a direct gesture. */ } };
  document.querySelector('#prev').onclick = () => show(current - 1);
  document.querySelector('#next').onclick = () => show(current + 1);
  document.querySelector('#notes-button').onclick = toggleNotes;
  document.querySelector('#close-notes').onclick = () => notes.hidden = true;
  document.querySelector('#fullscreen').onclick = fullscreen;
  document.querySelector('#overview').onclick = () => toc.showModal();
  document.querySelector('#close-toc').onclick = () => toc.close();
  slides.forEach((s, i) => {
    const b = document.createElement('button');
    b.textContent = `${i + 1}. ${s.querySelector('h1,h2').textContent}`;
    b.onclick = () => { show(i); toc.close(); };
    document.querySelector('#toc-links').append(b);
  });
  document.addEventListener('keydown', e => {
    if (['INPUT', 'TEXTAREA', 'SELECT', 'BUTTON', 'A'].includes(e.target.tagName) || e.target.isContentEditable || toc.open) return;
    const actions = {ArrowRight: () => show(current + 1), ArrowDown: () => show(current + 1), PageDown: () => show(current + 1), ' ': () => show(current + 1), Enter: () => show(current + 1), ArrowLeft: () => show(current - 1), ArrowUp: () => show(current - 1), PageUp: () => show(current - 1), Home: () => show(0), End: () => show(slides.length - 1), n: toggleNotes, N: toggleNotes, f: fullscreen, F: fullscreen, Escape: () => notes.hidden = true};
    if (actions[e.key]) { e.preventDefault(); actions[e.key](); }
  });
  document.querySelectorAll('[data-save]').forEach(el => {
    const key = `food-20260910-${el.dataset.save}`;
    try { el.value = localStorage.getItem(key) || ''; } catch { /* Local storage is optional. */ }
    el.addEventListener('input', () => { try { localStorage.setItem(key, el.value); } catch { /* Keep editing available. */ } });
  });
  document.querySelectorAll('.timer').forEach(timer => {
    const total = Number(timer.dataset.seconds);
    let left = total, end = 0, running = false;
    const toggle = timer.querySelector('[data-timer=toggle]');
    const render = () => { timer.querySelector('output').textContent = `${String(Math.floor(left / 60)).padStart(2, '0')}:${String(left % 60).padStart(2, '0')}`; timer.classList.toggle('finished', left === 0); toggle.textContent = running ? '暫停' : left === total ? '開始計時' : '繼續'; };
    toggle.onclick = () => { if (!running && left === 0) return; running = !running; if (running) end = Date.now() + left * 1000; render(); };
    timer.querySelector('[data-timer=reset]').onclick = () => { running = false; left = total; render(); };
    setInterval(() => { if (!running) return; left = Math.max(0, Math.ceil((end - Date.now()) / 1000)); if (!left) running = false; render(); }, 200);
  });
  addEventListener('resize', scale);
  addEventListener('hashchange', () => show(fromHash(), false));
  show(fromHash(), false); scale();
})();
