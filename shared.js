// ── CUSTOM CURSOR ──
const cur = document.getElementById('cur');
const ring = document.getElementById('ring');
let mx = 0, my = 0, rx = 0, ry = 0;

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cur.style.left = mx + 'px'; cur.style.top = my + 'px';
});

(function animRing() {
  rx += (mx - rx) * 0.13;
  ry += (my - ry) * 0.13;
  ring.style.left = rx + 'px'; ring.style.top = ry + 'px';
  requestAnimationFrame(animRing);
})();

document.querySelectorAll('a, button, .card').forEach(el => {
  el.addEventListener('mouseenter', () => {
    cur.style.transform = 'translate(-50%,-50%) scale(2.5)';
    ring.style.width = '54px'; ring.style.height = '54px';
    ring.style.borderColor = 'rgba(209,0,0,0.7)';
  });
  el.addEventListener('mouseleave', () => {
    cur.style.transform = 'translate(-50%,-50%) scale(1)';
    ring.style.width = '34px'; ring.style.height = '34px';
    ring.style.borderColor = 'rgba(209,0,0,0.45)';
  });
});

// ── LIGHTBOX ──
(function(){
  const lb = document.createElement('div');
  lb.className = 'lb';
  lb.innerHTML = '<button class="lb-btn lb-prev">&#8249;</button><img class="lb-img" alt="" /><button class="lb-btn lb-next">&#8250;</button><button class="lb-x">&#215;</button><span class="lb-count"></span>';
  document.body.appendChild(lb);

  let imgs = [], idx = 0;
  const lbImg = lb.querySelector('.lb-img');
  const lbCount = lb.querySelector('.lb-count');

  function show(i) {
    idx = (i + imgs.length) % imgs.length;
    lbImg.src = imgs[idx];
    lbCount.textContent = (idx + 1) + ' / ' + imgs.length;
  }
  function open(list, i) { imgs = list; lb.classList.add('open'); document.body.style.overflow = 'hidden'; show(i); }
  function close() { lb.classList.remove('open'); document.body.style.overflow = ''; }

  lb.querySelector('.lb-prev').addEventListener('click', () => show(idx - 1));
  lb.querySelector('.lb-next').addEventListener('click', () => show(idx + 1));
  lb.querySelector('.lb-x').addEventListener('click', close);
  lb.addEventListener('click', e => { if(e.target === lb) close(); });
  document.addEventListener('keydown', e => {
    if(!lb.classList.contains('open')) return;
    if(e.key === 'Escape') close();
    if(e.key === 'ArrowLeft') show(idx - 1);
    if(e.key === 'ArrowRight') show(idx + 1);
  });

  document.querySelectorAll('.c-gallery').forEach(gallery => {
    const as = [...gallery.querySelectorAll('a')];
    const srcs = as.map(a => a.href);
    as.forEach((a, i) => a.addEventListener('click', e => { e.preventDefault(); open(srcs, i); }));
  });
})();

// ── SCROLL REVEAL ──
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal, .reveal-l, .reveal-r').forEach(el => io.observe(el));
