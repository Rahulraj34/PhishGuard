// static/script.js
// Background particle network + fake live logs + scan pulse

// --------- Particle background ----------
(() => {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let w = canvas.width = innerWidth;
  let h = canvas.height = innerHeight;
  const DPR = window.devicePixelRatio || 1;
  canvas.width = w * DPR; canvas.height = h * DPR; canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
  ctx.scale(DPR, DPR);

  const N = Math.max(40, Math.floor((w*h)/90000)); // particle count relative to screen
  const nodes = [];
  for (let i=0;i<N;i++){
    nodes.push({
      x: Math.random()*w,
      y: Math.random()*h,
      vx: (Math.random()-0.5)*0.6,
      vy: (Math.random()-0.5)*0.6,
      r: 1 + Math.random()*1.6
    });
  }

  function draw(){
    ctx.clearRect(0,0,w,h);
    // subtle background glow
    ctx.fillStyle = "rgba(3,6,10,0.35)";
    ctx.fillRect(0,0,w,h);

    // connect nearby nodes
    for (let i=0;i<N;i++){
      const a = nodes[i];
      for (let j=i+1;j<N;j++){
        const b = nodes[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const d = Math.sqrt(dx*dx+dy*dy);
        if (d < 140){
          const alpha = 0.12 * (1 - d/140);
          ctx.strokeStyle = `rgba(0,255,153,${alpha})`;
          ctx.lineWidth = 0.6;
          ctx.beginPath();
          ctx.moveTo(a.x,a.y);
          ctx.lineTo(b.x,b.y);
          ctx.stroke();
        }
      }
    }

    // draw nodes
    for (let p of nodes){
      ctx.beginPath();
      ctx.fillStyle = `rgba(0,255,153,0.9)`;
      ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
      ctx.fill();
      p.x += p.vx; p.y += p.vy;
      if (p.x < -10) p.x = w+10; if (p.x > w+10) p.x = -10;
      if (p.y < -10) p.y = h+10; if (p.y > h+10) p.y = -10;
    }
    requestAnimationFrame(draw);
  }
  draw();

  window.addEventListener('resize', () => {
    w = canvas.width = innerWidth;
    h = canvas.height = innerHeight;
    canvas.width = w * DPR; canvas.height = h * DPR;
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    ctx.scale(DPR, DPR);
  });
})();


// --------- Scan pulse toggle when form submitted ----------
(() => {
  const form = document.querySelector('form');
  if (!form) return;
  form.addEventListener('submit', () => {
    // briefly add 'pulse' style to container for scanning feel
    const container = document.querySelector('.main-card');
    if (container){
      container.classList.add('pulse');
      setTimeout(()=> container.classList.remove('pulse'), 1400);
    }
    const custom = document.getElementById('live-log');
    if (custom){
      const t = new Date().toLocaleTimeString();
      const d = document.createElement('div');
      d.className = 'log-entry info';
      d.innerText = `[${t}] INFO — Checking URL...`;
      custom.prepend(d);
      while (custom.children.length > 30) custom.removeChild(custom.lastChild);
    }
  });
})();