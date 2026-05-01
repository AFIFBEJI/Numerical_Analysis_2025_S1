// ─────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────
function K(tex, block){
  try{ return katex.renderToString(tex,{throwOnError:false,displayMode:!!block}); }
  catch(e){ return tex; }
}
function KE(el){
  if(!el) return;
  renderMathInElement(el,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});
}
function r4(v){ return Math.round(v*10000)/10000; }
function fmt(v){ if(Number.isInteger(v)) return String(v); return r4(v).toString(); }
function rnd(a,b){ return Math.floor(Math.random()*(b-a+1))+a; }
function clamp(v,min,max){ return Math.min(max,Math.max(min,v)); }
function hexToRgb(hex){
  const h=(hex||'').replace('#','').trim();
  if(!/^[0-9a-fA-F]{6}$/.test(h)) return {r:14,g:14,b:16};
  return {
    r:parseInt(h.slice(0,2),16),
    g:parseInt(h.slice(2,4),16),
    b:parseInt(h.slice(4,6),16)
  };
}
function rgbToHex(r,g,b){
  const p=(n)=>clamp(Math.round(n),0,255).toString(16).padStart(2,'0');
  return `#${p(r)}${p(g)}${p(b)}`;
}
function mixHex(a,b,t){
  const A=hexToRgb(a), B=hexToRgb(b), m=clamp(t,0,1);
  return rgbToHex(A.r+(B.r-A.r)*m,A.g+(B.g-A.g)*m,A.b+(B.b-A.b)*m);
}
function luminance(hex){
  const {r,g,b}=hexToRgb(hex);
  return (0.2126*r+0.7152*g+0.0722*b)/255;
}
function applyTheme(bg,accent){
  const root=document.documentElement;
  const dark=luminance(bg)<0.55;
  const bg2=mixHex(bg,dark?'#ffffff':'#000000',dark?0.05:0.04);
  const bg3=mixHex(bg,dark?'#ffffff':'#000000',dark?0.09:0.08);
  const card=mixHex(bg,dark?'#ffffff':'#000000',dark?0.07:0.06);
  const border=mixHex(bg,dark?'#ffffff':'#000000',dark?0.15:0.16);
  const border2=mixHex(bg,dark?'#ffffff':'#000000',dark?0.2:0.22);
  const accent2=mixHex(accent,dark?'#ffffff':'#000000',dark?0.22:0.16);
  root.style.setProperty('--bg',bg);
  root.style.setProperty('--bg2',bg2);
  root.style.setProperty('--bg3',bg3);
  root.style.setProperty('--card',card);
  root.style.setProperty('--border',border);
  root.style.setProperty('--border2',border2);
  root.style.setProperty('--accent',accent);
  root.style.setProperty('--accent2',accent2);
  root.style.setProperty('--text',dark?'#e8e8f0':'#121218');
  root.style.setProperty('--text2',dark?'#a0a0b4':'#3a3a48');
  root.style.setProperty('--text3',dark?'#606078':'#5d5d70');
}
function settingsThemeChanged(){
  const bgEl=document.getElementById('set-bg');
  const acEl=document.getElementById('set-accent');
  if(!bgEl||!acEl) return;
  const bg=bgEl.value||'#0e0e10';
  const accent=acEl.value||'#e2b714';
  applyTheme(bg,accent);
  try{ localStorage.setItem('ni-theme',JSON.stringify({bg,accent})); }catch(e){}
}
function settingsResetTheme(){
  const bg='#0e0e10', accent='#e2b714';
  applyTheme(bg,accent);
  const bgEl=document.getElementById('set-bg');
  const acEl=document.getElementById('set-accent');
  if(bgEl) bgEl.value=bg;
  if(acEl) acEl.value=accent;
  try{ localStorage.setItem('ni-theme',JSON.stringify({bg,accent})); }catch(e){}
}
function themeInit(){
  let bg='#0e0e10', accent='#e2b714';
  try{
    const raw=localStorage.getItem('ni-theme');
    if(raw){
      const obj=JSON.parse(raw);
      if(obj&&obj.bg&&obj.accent){ bg=obj.bg; accent=obj.accent; }
    }
  }catch(e){}
  applyTheme(bg,accent);
  const bgEl=document.getElementById('set-bg');
  const acEl=document.getElementById('set-accent');
  if(bgEl) bgEl.value=bg;
  if(acEl) acEl.value=accent;
}

function genPoints(n){
  const xs=[];
  while(xs.length<n){const x=rnd(-5,5); if(!xs.includes(x)) xs.push(x);}
  xs.sort((a,b)=>a-b);
  return xs.map(x=>({x,y:rnd(-8,8)}));
}
function ddTable(pts){
  const n=pts.length, t=Array.from({length:n},()=>new Array(n).fill(null));
  for(let i=0;i<n;i++) t[i][0]=pts[i].y;
  for(let j=1;j<n;j++) for(let i=0;i<n-j;i++) t[i][j]=(t[i+1][j-1]-t[i][j-1])/(pts[i+j].x-pts[i].x);
  return t;
}
function evalNewton(pts,t,x){
  let res=0,basis=1;
  for(let k=0;k<pts.length;k++){res+=t[0][k]*basis; basis*=(x-pts[k].x);}
  return res;
}
function evalNewtonOrd(pts,t,x,ord){
  let res=0,basis=1;
  for(let k=0;k<=ord;k++){res+=t[0][k]*basis; basis*=(x-pts[k].x);}
  return res;
}
function polyLatex(pts,t){
  const n=pts.length; if(!n) return '';
  let s='P(x)='+fmt(r4(t[0][0])); let bTex='';
  for(let k=1;k<n;k++){
    const xk=pts[k-1].x, c=r4(t[0][k]);
    const sg=xk>=0?'-':'+', ax=fmt(Math.abs(xk));
    bTex+=`(x ${sg} ${ax})`;
    const sg2=c>=0?'+':'-';
    s+=` ${sg2} ${fmt(Math.abs(c))}\\,${bTex}`;
  }
  return s;
}
function polyLatexOrd(pts,t,ord){
  const n=pts.length; if(!n) return '';
  let s='P(x)='+fmt(r4(t[0][0])); let bTex='';
  for(let k=1;k<=ord&&k<n;k++){
    const xk=pts[k-1].x, c=r4(t[0][k]);
    const sg=xk>=0?'-':'+', ax=fmt(Math.abs(xk));
    bTex+=`(x ${sg} ${ax})`;
    const sg2=c>=0?'+':'-';
    s+=` ${sg2} ${fmt(Math.abs(c))}\\,${bTex}`;
  }
  return s;
}

// screen router
let _vizInit=false;
let _expTimer=null;
function go(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.getElementById('screen-'+id).classList.add('active');
  const quickMenuBtn=document.getElementById('quick-menu-btn');
  if(quickMenuBtn) quickMenuBtn.style.display=(id==='menu')?'none':'inline-flex';
  if(id!=='advanced') clearInterval(_expTimer);
  if(id==='tutorial') tutInit();
  if(id==='tut-game') tgInit();
  if(id==='advanced') expInit();
  if(id==='viz'){if(!_vizInit){_vizInit=true;vizInit();} else vizRender();}
  if(id==='challenge') chReset();
  if(id==='menu'){ clearInterval(_advTimer); clearInterval(_chTimer); clearInterval(_expTimer); }
}

// feedback helper
function showFB(id,msg,type){
  const el=document.getElementById(id);
  if(!el) return;
  el.textContent=msg; el.className=`fb show fb-${type}`;
  clearTimeout(el._t); el._t=setTimeout(()=>el.classList.remove('show'),2200);
}

// result overlay
function showResult({emoji,title,sub,ok,err,time,score,btns}){
  document.getElementById('res-emoji').textContent=emoji;
  document.getElementById('res-title').textContent=title;
  document.getElementById('res-sub').textContent=sub;
  document.getElementById('res-ok').textContent=ok;
  document.getElementById('res-err').textContent=err;
  document.getElementById('res-time').textContent=time;
  document.getElementById('res-score').textContent=score;
  document.getElementById('res-btns').innerHTML=btns.map(b=>`<button class="btn btn-primary" onclick="${b.fn}">${b.lbl}</button>`).join('');
  document.getElementById('res-overlay').style.display='flex';
}
function hideResult(){ document.getElementById('res-overlay').style.display='none'; }

function scoreFlash(txt,pos){
  const el=document.createElement('div');
  el.className=`score-flash ${pos?'sf-plus':'sf-minus'}`; el.textContent=txt;
  document.body.appendChild(el); setTimeout(()=>el.remove(),850);
}
function doShake(id){ const el=document.getElementById(id); if(!el) return; el.classList.add('shake'); setTimeout(()=>el.classList.remove('shake'),400); }

// explainer screen (replaces advanced levels)
const EXP_DATA={
  theory:[
    {title:'What interpolation really means',body:'Interpolation is not guessing blindly; it is a structured reconstruction of a function from known samples. In Newton interpolation, we assume the data points are trustworthy and we build a polynomial that passes exactly through all of them, not approximately. This is useful when you need values between measured points and want a method that is mathematically consistent. The most important student intuition is this: each point constrains the curve, and the final polynomial is simply the smoothest algebraic object that satisfies all those constraints simultaneously.'},
    {title:'Why divided differences are powerful',body:'Divided differences are the engine that turns raw point data into polynomial coefficients. Instead of solving a large linear system every time, you build a triangular table where each new entry is computed from nearby values in the previous order. This local reuse makes the method efficient, easier to debug, and easier to teach because each step has a clear origin. Conceptually, first-order differences act like slopes, second-order differences capture change of slope, and higher orders progressively capture finer shape behavior. That layered interpretation is exactly why students can connect the table to the final curve shape.'},
    {title:'Newton form and incremental learning',body:'The Newton polynomial is written as a sum of terms that grow step by step: a constant term, then a linear correction, then a quadratic correction, then a cubic correction, and so on. This structure is pedagogically excellent because students can stop at any order and still have a valid approximation. It also mirrors computational practice: when a new point arrives, you only append one new coefficient term rather than recomputing everything. In real analysis workflows, this incremental nature is one of the strongest reasons Newton form is preferred over more rigid formulations.'},
  ],
  practice:[
    {title:'Step 1: Set the data carefully',body:'Start by sorting points by x and writing them in the first column. Then copy all y values into Order 0. Before computing anything else, confirm that every x is unique; this single check prevents denominator mistakes later. Students should treat this step as setup discipline: if the table is clean at the start, every later step becomes easier and fewer arithmetic errors propagate.'},
    {title:'Step 2: Build ORD1 with full traceability',body:'For each ORD1 entry, take the difference of adjacent y values and divide by the corresponding x-gap. Keep the numerator and denominator visible while computing; this develops procedural confidence and helps you catch sign mistakes immediately. In our animated table, this appears as cell-by-cell movement where source values are highlighted first, then the new cell is filled, exactly like a guided GIF walkthrough.'},
    {title:'Step 3: Repeat the same logic for higher orders',body:'ORD2 and beyond use the same recipe, but now the numerator comes from the previous order column. This is where students usually think the method changed, but it did not; only the source column changed. Reading the process as a repeated pattern rather than a new formula every time dramatically reduces cognitive load and makes larger tables manageable.'},
    {title:'Step 4: Build and verify the polynomial',body:'Take top-diagonal coefficients and assemble the Newton form term by term. After each added term, test on at least one known point to ensure consistency. This creates a practical loop: compute, assemble, verify. When students adopt this habit, they understand both theory and practice because they can explain not just what the final polynomial is, but exactly how each table cell contributed to it.'},
  ]
};
const EXP_MERGED=[
  ...EXP_DATA.theory.map((item)=>({kind:'Concept',...item})),
  ...EXP_DATA.practice.map((item)=>({kind:'How-to',...item}))
];
const EXP_FRAMES=[
  {
    label:'Frame 1/5 - Setup points and Order 0',
    table:[
      ['x','Ord0','Ord1','Ord2','Ord3'],
      ['-2','3','','',''],
      ['0','-1','','',''],
      ['1','2','','',''],
      ['3','5','','','']
    ],
    hi:[[1,1],[2,1],[3,1],[4,1]],
    nw:[],
    flow:{from:['y0','y1','y2','y3'],to:'Order 0 column',expr:'Copy known y values into Ord0'}
  },
  {
    label:'Frame 2/5 - Compute first ORD1 cell from Ord0 values',
    table:[
      ['x','Ord0','Ord1','Ord2','Ord3'],
      ['-2','3','-2','',''],
      ['0','-1','','',''],
      ['1','2','','',''],
      ['3','5','','','']
    ],
    hi:[[1,1],[2,1]],
    nw:[[1,2]],
    flow:{from:['y1','y0','x1','x0'],to:'Ord1[0]',expr:'(y1 - y0) / (x1 - x0)'}
  },
  {
    label:'Frame 3/5 - Fill remaining ORD1 cells',
    table:[
      ['x','Ord0','Ord1','Ord2','Ord3'],
      ['-2','3','-2','',''],
      ['0','-1','3','',''],
      ['1','2','1.5','',''],
      ['3','5','','','']
    ],
    hi:[[2,1],[3,1],[4,1]],
    nw:[[2,2],[3,2]],
    flow:{from:['y2','y1','x2','x1'],to:'Ord1[1] then Ord1[2]',expr:'Repeat same slope pattern'}
  },
  {
    label:'Frame 4/5 - Build ORD2 from ORD1',
    table:[
      ['x','Ord0','Ord1','Ord2','Ord3'],
      ['-2','3','-2','1.6667',''],
      ['0','-1','3','-0.5',''],
      ['1','2','1.5','',''],
      ['3','5','','','']
    ],
    hi:[[1,2],[2,2],[3,2]],
    nw:[[1,3],[2,3]],
    flow:{from:['Ord1[1]','Ord1[0]','x2','x0'],to:'Ord2[0]',expr:'(Ord1[1] - Ord1[0]) / (x2 - x0)'},
    trick:'Denominator trick: for the next order, take the FIRST x from the upper term and the LAST x from the lower term.'
  },
  {
    label:'Frame 5/5 - Final ORD3 and completed table',
    table:[
      ['x','Ord0','Ord1','Ord2','Ord3'],
      ['-2','3','-2','1.6667','-0.5417'],
      ['0','-1','3','-0.5',''],
      ['1','2','1.5','',''],
      ['3','5','','','']
    ],
    hi:[[1,3],[2,3]],
    nw:[[1,4]],
    flow:{from:['Ord2[1]','Ord2[0]','x3','x0'],to:'Ord3[0]',expr:'(Ord2[1] - Ord2[0]) / (x3 - x0)'},
    trick:'Example trick in action: from (y2-y1)/(x2-x1) and (y3-y2)/(x3-x2), denominator becomes x3 - x1.'
  }
];
const EXP_CURVE_FRAMES=[
  {ord:1,path:'M15 98 L120 62 L225 74 L315 36',note:'ORD1: piecewise linear behavior dominates.'},
  {ord:2,path:'M15 98 Q95 44 175 70 T315 36',note:'ORD2: first curvature correction is added.'},
  {ord:3,path:'M15 98 C85 30 160 92 315 36',note:'ORD3: richer shape with higher-order correction.'},
  {ord:'Final',path:'M15 98 C70 25 155 100 220 64 C252 45 284 42 315 36',note:'Final: complete Newton polynomial fit.'}
];
let EXP_ANIM=0;
function expInit(){
  EXP_ANIM=0;
  expRender();
  expRenderFrame();
  clearInterval(_expTimer);
  _expTimer=setInterval(()=>{
    EXP_ANIM=(EXP_ANIM+1)%EXP_FRAMES.length;
    expRenderFrame();
  },2200);
}
function expRenderFrame(){
  const frame=EXP_FRAMES[EXP_ANIM];
  const holder=document.getElementById('exp-gif-table');
  const lbl=document.getElementById('exp-gif-eq');
  if(!holder||!lbl) return;
  lbl.textContent='Example points: (-2,3), (0,-1), (1,2), (3,5)';
  let html='<div class="exp-gif-table-wrap"><table class="exp-gif-table"><thead><tr><th>x</th><th>Ord0</th><th>Ord1</th><th>Ord2</th><th>Ord3</th></tr></thead><tbody>';
  html+='<tr><td>-2</td><td>3</td><td>-2</td><td>1.6667</td><td>-0.5417</td></tr>';
  html+='<tr><td>0</td><td>-1</td><td>3</td><td>-0.5</td><td><span class="exp-gif-muted">-</span></td></tr>';
  html+='<tr><td>1</td><td>2</td><td>1.5</td><td><span class="exp-gif-muted">-</span></td><td><span class="exp-gif-muted">-</span></td></tr>';
  html+='<tr><td>3</td><td>5</td><td><span class="exp-gif-muted">-</span></td><td><span class="exp-gif-muted">-</span></td><td><span class="exp-gif-muted">-</span></td></tr>';
  html+='</tbody></table></div>';
  html+='<div class="exp-flow"><div class="exp-flow-expr">Read coefficients directly from the top diagonal: a0 = 3, a1 = -2, a2 = 1.6667, a3 = -0.5417.</div></div>';
  holder.innerHTML=html;
  const curveEl=document.getElementById('exp-gif-curve');
  if(curveEl){
    const cf=EXP_CURVE_FRAMES[EXP_ANIM%EXP_CURVE_FRAMES.length];
    curveEl.innerHTML=`
      <div class="exp-mini-stage">
        <svg class="exp-curve-svg" viewBox="0 0 330 130" preserveAspectRatio="xMidYMid meet">
          <path d="M10 110 L320 110" stroke="#353540" stroke-width="1" fill="none"></path>
          <path d="M10 10 L10 112" stroke="#353540" stroke-width="1" fill="none"></path>
          <path class="exp-curve-path" d="${cf.path}"></path>
          <circle class="exp-curve-pts" cx="15" cy="98" r="4"></circle>
          <circle class="exp-curve-pts" cx="120" cy="62" r="4"></circle>
          <circle class="exp-curve-pts" cx="225" cy="74" r="4"></circle>
          <circle class="exp-curve-pts" cx="315" cy="36" r="4"></circle>
        </svg>
      </div>
      <div class="exp-mini-note">Order stage: ${cf.ord}. ${cf.note}</div>
    `;
  }
  const diagEl=document.getElementById('exp-gif-diag');
  if(diagEl){
    const ord=Math.min(3,EXP_ANIM);
    const coeffs=['3','-2','1.6667','-0.5417'];
    const coeffHtml=coeffs.map((v,i)=>`<span class="exp-chip ${i<=ord?'exp-chip-target':''}">a${i}=${v}</span>`).join(' ');
    diagEl.innerHTML=`
      <div class="exp-mini-stage"><div class="exp-basis-term">${coeffHtml}</div></div>
      <div class="exp-mini-note">Take coefficients from the top diagonal: a0, a1, a2, a3.</div>
    `;
  }
  const formulaEl=document.getElementById('exp-gif-formula');
  if(formulaEl){
    const ord=Math.min(3,EXP_ANIM);
    const terms=[
      'P(x)=3',
      'P(x)=3 - 2<span class="hot">(x+2)</span>',
      'P(x)=3 - 2(x+2) + 1.6667<span class="hot">(x+2)(x-0)</span>',
      'P(x)=3 - 2(x+2) + 1.6667(x+2)(x-0) - 0.5417<span class="hot">(x+2)(x-0)(x-1)</span>'
    ];
    formulaEl.innerHTML=`
      <div class="exp-mini-stage"><div class="exp-basis-term">${terms[ord]}</div></div>
      <div class="exp-mini-note">Build the Newton polynomial term by term as new orders appear.</div>
    `;
  }
}
function expRender(){
  const b=document.getElementById('exp-body'); if(!b) return;
  const rows=EXP_MERGED.map((s,i)=>`
    <div class="exp-card" style="animation-delay:${i*0.06}s">
      <div class="exp-card-kicker">${s.kind} ${i+1}</div>
      <div class="exp-card-title">${s.title}</div>
      <div class="exp-card-body">${s.body}</div>
    </div>
  `).join('');
  b.innerHTML=`<div class="exp-grid">${rows}</div>`;
}

// ─────────────────────────────────────────────
// TUTORIAL STEPS
// ─────────────────────────────────────────────
const STEPS=[
{title:'What You Need To Know',html:`
<p><span class="highlight">Goal:</span> build one polynomial that passes through all given points.</p>
<div class="formula-block">$$P(x_i)=y_i$$</div>
<p>If this is true for every point, your interpolation is correct.</p>
`},
{title:'Data Rules',html:`
<p>Use points $(x_i,y_i)$ with <span class="highlight">all x-values different</span>.</p>
<p>If two points share the same x, divided differences break (division by zero).</p>
`},
{title:'Table Idea',html:`
<p>Column 0 is just y-values. Next columns are computed from previous column values.</p>
<div class="formula-block">$$f[x_i,x_{i+1}]=\\dfrac{f[x_{i+1}]-f[x_i]}{x_{i+1}-x_i}$$</div>
<p>Same pattern repeats for higher orders.</p>
`},
{title:'Where Coefficients Come From',html:`
<p>Take the top diagonal of the table. Those are Newton coefficients:</p>
<div class="formula-block">$$a_k=f[x_0,\\ldots,x_k]$$</div>
<p>Then build polynomial term by term.</p>
`},
{title:'Newton Form (Practical)',html:`
<div class="formula-block">$$P(x)=a_0+a_1(x-x_0)+a_2(x-x_0)(x-x_1)+\\cdots$$</div>
<p><span class="highlight-green">Practical benefit:</span> adding one new point means adding one new term only.</p>
`},
{title:'Now Practice',html:`
<p>In the guided game you will pick source cells and fill each divided-difference cell step by step.</p>
<p>Focus on numerator first, denominator second, then confirm the value.</p>
`}
];

let tutStep=0;
function tutInit(){ tutStep=0; tutRender(); }
function tutNav(d){
  if(d===1 && tutStep===STEPS.length-1){ go('tut-game'); return; }
  tutStep=Math.max(0,Math.min(STEPS.length-1,tutStep+d));
  tutRender();
}
function tutRender(){
  const s=STEPS[tutStep];
  const body=document.getElementById('tut-body');
  body.innerHTML=`<div class="tut-card"><div class="step-label">Step ${tutStep+1} of ${STEPS.length}</div><div class="step-title">${s.title}</div><div class="step-body">${s.html}</div></div>`;
  KE(body);
  document.getElementById('tut-prog-lbl').textContent=`${tutStep+1} / ${STEPS.length}`;
  document.getElementById('tut-dots').innerHTML=STEPS.map((_,i)=>`<div class="prog-dot ${i<tutStep?'done':i===tutStep?'active':''}"></div>`).join('');
  document.getElementById('tut-prev').disabled=(tutStep===0);
  const nx=document.getElementById('tut-next');
  nx.textContent=tutStep===STEPS.length-1?'▶ Start Game':'Next →';
}

// ─────────────────────────────────────────────
// TUTORIAL GAME
// ─────────────────────────────────────────────
let TG={};
function tgInit(){ tgNewRound(); }
function tgShuffle(arr){
  const a=[...arr];
  for(let i=a.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }
  return a;
}
function tgBasisSym(k){
  if(k===0) return '1';
  let out='';
  for(let i=0;i<k;i++) out+=`(x-x${i})`;
  return out;
}
function tgBasisLatex(k){
  if(k===0) return '\\omega_0(x)=1';
  let out=`\\omega_${k}(x)=`;
  for(let i=0;i<k;i++) out+=`(x-x_${i})`;
  return out;
}
function tgFactorLatexFromX(x){
  const xv=r4(x);
  if(xv>=0) return `(x-${fmt(xv)})`;
  return `(x+${fmt(Math.abs(xv))})`;
}
function tgOmegaLatexWithPicks(k,picks){
  if(k===0) return '\\omega_0(x)=1';
  let out=`\\omega_${k}(x)=`;
  for(let i=0;i<k;i++){
    if(i<picks.length){
      const idx=picks[i];
      out+=tgFactorLatexFromX(TG.pts[idx].x);
    } else {
      out+='(x-\\color{orange}{?})';
    }
  }
  return out;
}
function tgCoeffTermSym(k){
  const c=r4(TG.t[0][k]);
  if(k===0) return fmt(c);
  const s=c>=0?'+':'-';
  return `${s} ${fmt(Math.abs(c))} ${tgBasisSym(k)}`;
}
function tgOmegaValueLatex(k){
  if(k===0) return '\\times 1';
  let out='';
  for(let i=0;i<k;i++) out+=tgFactorLatexFromX(TG.pts[i].x);
  return out;
}
function tgCoeffLatex(k){
  const c=r4(TG.t[0][k]);
  if(k===0) return fmt(c);
  return `${c>=0?'+':'-'}\\,${fmt(Math.abs(c))}`;
}
function tgNewRound(){
  const pts=genPoints(4), t=ddTable(pts), n=4;
  const rev=Array.from({length:n},()=>new Array(n).fill(false));
  for(let i=0;i<n;i++) rev[i][0]=true;
  TG={
    pts,t,n,rev,
    ci:0,cj:1,step:0,sel:[],
    phase:'terms',
    termsStep:1,
    termsPlaced:[tgBasisLatex(0)],
    termsPick:[],
    polyStep:0,
    polyPlaced:[],
    ok:0
  };
  tgRender();
}
function tgStartTable(){
  TG.phase='table';
  Object.assign(TG,{ci:0,cj:1,step:0,sel:[],tableDone:false});
  tgRender();
}
function tgStartPoly(){
  TG.phase='poly';
  TG.polyStep=0; // legacy
  TG.polyPlaced=[]; // legacy
  TG.polyTokenStep=0;
  TG.polyTokenPlaced=[];
  tgRender();
}
function tgFinishTutorial(){
  TG.phase='done';
  tgRender();
}
function tgAdvanceTarget(){
  let {ci,cj,n}=TG;
  ci++; if(ci>n-cj-1){cj++;ci=0;}
  if(cj>=n){
    TG.tableDone=true;
    tgRender();
    return;
  }
  Object.assign(TG,{ci,cj,step:0,sel:[]});
  tgRender();
}
function tgAllowDrop(ev){ ev.preventDefault(); }
function tgDragStart(ev){
  const kind=ev.target.dataset.kind||'';
  const val=ev.target.dataset.val||'';
  const idx=ev.target.dataset.idx||'';
  ev.dataTransfer.setData('text/plain',JSON.stringify({kind,val,idx}));
}
function tgDrop(ev,target){
  ev.preventDefault();
  const raw=ev.dataTransfer.getData('text/plain');
  if(!raw) return;
  let data=null;
  try{ data=JSON.parse(raw); }catch(e){ return; }
  if(!data) return;
  if(target==='terms' && TG.phase==='terms'){
    const right=tgBasisSym(TG.termsStep);
    if(data.kind==='basis' && data.val===right){
      TG.termsPlaced.push(right); TG.termsStep++; TG.ok++;
      showFB('tg-fb','Good. Next basis term.','ok');
      if(TG.termsStep>=TG.n) showFB('tg-fb','Basis part complete. Press Next.','ok');
    } else {
      showFB('tg-fb','Not the right basis term yet.','err');
    }
    tgRender();
  }
  if(target==='poly' && TG.phase==='poly'){
    const s=TG.polyTokenStep||0;
    const k=Math.floor(s/2);
    const wantKind=(s%2===0)?'coeff':'omega';
    const gotK=Number(data.idx);
    if(data.kind===wantKind && gotK===k){
      const tok=(wantKind==='coeff')?tgCoeffLatex(k):tgOmegaValueLatex(k);
      TG.polyTokenPlaced.push(tok);
      TG.polyTokenStep++;
      TG.ok++;
      showFB('tg-fb',`Correct ${wantKind} token.`,'ok');
      if((TG.polyTokenStep||0)>=TG.n*2){ tgFinishTutorial(); return; }
    } else {
      const nextK=Math.floor((TG.polyTokenStep||0)/2);
      const nextKind=((TG.polyTokenStep||0)%2===0)?'coefficient':'omega term';
      showFB('tg-fb',`Pick ${nextKind} #${nextK} next.`,'err');
    }
    tgRender();
  }
}
function tgRenderTerms(){
  const step=TG.termsStep;
  const done=step>=TG.n;
  const triRows=Array.from({length:TG.n},(_,k)=>{
    if(k===0) return tgBasisLatex(0);
    if(k<step) return tgBasisLatex(k);
    if(k===step && !done) return tgOmegaLatexWithPicks(k,TG.termsPick||[]);
    return tgOmegaLatexWithPicks(k,[]);
  });
  let ptsTbl='<div class="dd-wrap"><table class="dd-table tg-pts-table" style="min-width:340px;"><thead><tr><th class="tg-idx-sm">Index</th><th>x</th><th>y</th></tr></thead><tbody>';
  for(let i=0;i<TG.n;i++){
    const exp=!done?(TG.termsPick||[]).length:-1;
    const xCls=(i===exp&&!done)?'cell-source tg-x-target':'';
    ptsTbl+=`<tr><td class="cell-index tg-idx-sm">${i}</td><td class="cell-known ${xCls}" onclick="tgPickOmegaX(${i})">${fmt(TG.pts[i].x)}</td><td class="cell-known">${fmt(TG.pts[i].y)}</td></tr>`;
  }
  ptsTbl+='</tbody></table></div>';
  const c=document.getElementById('tg-content');
  c.innerHTML=`
<div class="target-box">
  <div class="target-label">Step 1 — Build Omega Terms</div>
  <div style="font-size:.76rem;color:var(--text2);margin-bottom:8px;">Use the points table to fill each omega term in order.</div>
  ${ptsTbl}
  <div class="omega-tri">
    ${triRows.map((r,k)=>`<div class="omega-row ${(!done&&k===step)?'omega-row-active':''}">${K(r,false)}</div>`).join('')}
  </div>
  <div style="font-size:.82rem;overflow-x:auto;margin-top:8px;">${done?K('All\\;\\omega\\;terms\\;completed.',false):K(`Currently\\;filling\\;\\omega_${step}(x).`,false)}</div>
</div>
<div class="fb" id="tg-fb"></div>
<div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
  ${done?'<button class="btn btn-primary" onclick="tgStartTable()">Next: Divided-Difference Table →</button>':''}
  <button class="btn btn-secondary" onclick="tgNewRound()">Restart</button>
</div>`;
}
function tgPickOmegaX(idx){
  if(TG.phase!=='terms') return;
  const step=TG.termsStep;
  const expected=(TG.termsPick||[]).length;
  if(idx===expected){
    TG.termsPick.push(idx);
    showFB('tg-fb',`Picked x_${idx}.`,'ok');
    if(TG.termsPick.length===step){
      TG.termsPlaced.push(tgBasisLatex(step));
      TG.termsStep++;
      TG.termsPick=[];
      TG.ok++;
      showFB('tg-fb',`ω${step} completed.`,'ok');
      if(TG.termsStep>=TG.n) showFB('tg-fb','Omega part complete. Press Next.','ok');
    }
  } else {
    showFB('tg-fb',`Pick x_${expected} first for this term.`,'err');
  }
  tgRender();
}
function tgRenderTable(){
  const {pts,t,n,rev,ci,cj,step,sel}=TG;
  const cv=[r4(t[ci+1][cj-1]),r4(t[ci][cj-1]),r4(pts[ci+cj].x),r4(pts[ci].x)];
  TG.cv=cv;
  const slots={
    nt:{row:ci+cj,col:cj-1,val:cv[0],label:'numerator top'},
    nb:{row:ci+cj-1,col:cj-1,val:cv[1],label:'numerator bottom'},
    xt:{row:ci+cj,col:'x',val:cv[2],label:'x top'},
    xb:{row:ci,col:'x',val:cv[3],label:'x bottom'}
  };
  const slotOrder=['nt','nb','xt','xb'];
  const liveFml=()=>{
    const token=(k)=>k<sel.length?fmt(sel[k]):k===step?'<span class="hot">?</span>':'?';
    return `<span class="frac"><span class="num">(${token(0)})-(${token(1)})</span><span class="den">(${token(2)})-(${token(3)})</span></span>`;
  };
  let tbl='<div class="dd-wrap"><table class="dd-table tg-dd-table"><thead><tr><th class="idx-col">Index</th><th>x</th><th>f[xᵢ]</th>';
  for(let j=1;j<n;j++) tbl+=`<th>Order ${j}</th>`;
  tbl+='</tr></thead><tbody>';
  for(let i=0;i<n;i++){
    tbl+=`<tr><td class="cell-index idx-col">${i}</td>`;
    const xToken=(step===2&&i===slots.xt.row)?'xt':(step===3&&i===slots.xb.row)?'xb':'';
    tbl+=`<td class="cell-known ${xToken?'cell-source':''}" ${xToken?`onclick="tgPick('${xToken}')"`:''}>${fmt(pts[i].x)}</td>`;
    for(let j=0;j<n;j++){
      if(j===0){
        const yToken=(cj-1===0&&step===0&&i===slots.nt.row)?'nt':(cj-1===0&&step===1&&i===slots.nb.row)?'nb':'';
        tbl+=`<td class="cell-known ${yToken?'cell-source':''}" ${yToken?`onclick="tgPick('${yToken}')"`:''}>${fmt(t[i][0])}</td>`;
        continue;
      }
      if(i<j){tbl+='<td class="cell-empty"></td>';continue;}
      const ti=i-j;
      const ddToken=(j===cj-1&&step===0&&i===slots.nt.row)?'nt':(j===cj-1&&step===1&&i===slots.nb.row)?'nb':'';
      if(rev[ti][j]){
        const a=fmt(r4(t[ti+1][j-1])), b=fmt(r4(t[ti][j-1])), c=fmt(r4(pts[ti+j].x)), d=fmt(r4(pts[ti].x));
        tbl+=`<td class="cell-revealed tg-cell-revealed ${ddToken?'cell-source':''}" ${ddToken?`onclick="tgPick('${ddToken}')"`:''}>${fmt(r4(t[ti][j]))}<div class="cell-note"><span class="frac"><span class="num">(${a})-(${b})</span><span class="den">(${c})-(${d})</span></span></div></td>`;
      } else if(ti===ci&&j===cj){
        tbl+=`<td class="cell-target"><div class="cell-live-formula">${liveFml()}</div><div class="cell-prompt">Click source cell for: ${slots[slotOrder[step]].label}</div></td>`;
      } else tbl+=`<td class="cell-hidden">?</td>`;
    }
    tbl+='</tr>';
  }
  tbl+='</tbody></table></div>';
  const fTex=`f[x_{${ci}},\\ldots,x_{${ci+cj}}]=\\dfrac{${fmt(r4(t[ci+1][cj-1]))}-(${fmt(r4(t[ci][cj-1]))})}{${fmt(pts[ci+cj].x)}-${fmt(pts[ci].x)}}=${fmt(r4(t[ci][cj]))}`;
  const c=document.getElementById('tg-content');
  c.innerHTML=`
${tbl}
<div class="target-box">
  <div class="target-label">Step 2 — Complete the Divided-Difference Table</div>
  ${TG.tableDone
    ? '<div style="font-size:.75rem;color:var(--green);margin-top:4px;">Table complete. Press Next to continue.</div>'
    : '<div id="tg-fml" style="font-size:.9rem;overflow-x:auto;margin:8px 0;"></div><div style="font-size:.75rem;color:var(--blue);margin-top:4px;">Click values directly inside the highlighted table cell.</div>'
  }
</div>
<div class="fb" id="tg-fb"></div>
<div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
  ${TG.tableDone?'<button class="btn btn-primary" onclick="tgStartPoly()">Next: Build P(x) →</button>':''}
  <button class="btn btn-secondary" onclick="tgNewRound()">Restart</button>
</div>`;
  const fEl=document.getElementById('tg-fml');
  if(fEl && !TG.tableDone) fEl.innerHTML=K(fTex,false);
}
function tgRenderPoly(){
  const done=(TG.polyTokenStep||0)>=TG.n*2;
  const nextK=Math.floor((TG.polyTokenStep||0)/2);
  const nextKind=((TG.polyTokenStep||0)%2===0)?'coefficient':'omega term';
  const built=(TG.polyTokenPlaced||[]).join('\\,');
  let coeffTbl='<div class="dd-wrap"><table class="dd-table" style="min-width:360px;"><thead><tr><th>Index</th><th>x</th><th>f[x]</th>';
  for(let j=1;j<TG.n;j++) coeffTbl+=`<th>Order ${j}</th>`;
  coeffTbl+='</tr></thead><tbody>';
  for(let i=0;i<TG.n;i++){
    coeffTbl+=`<tr><td class="cell-index">${i}</td><td class="cell-known">${fmt(TG.pts[i].x)}</td>`;
    for(let j=0;j<TG.n;j++){
      if(j===0){
        const isTop=i===0;
        const k=0;
        const active=(!done && nextKind==='coefficient' && nextK===k && isTop)?'cell-source tg-x-target':'';
        coeffTbl+=`<td class="cell-known ${active}" draggable="true" data-kind="coeff" data-idx="${isTop?k:-1}" ondragstart="tgDragStart(event)">${fmt(r4(TG.t[i][0]))}</td>`;
        continue;
      }
      if(i<j){ coeffTbl+='<td class="cell-empty"></td>'; continue; }
      const ti=i-j;
      const val=r4(TG.t[ti][j]);
      const isTop=ti===0;
      const k=j;
      const active=(!done && nextKind==='coefficient' && nextK===k && isTop)?'cell-source tg-x-target':'';
      coeffTbl+=`<td class="cell-revealed ${active}" draggable="true" data-kind="coeff" data-idx="${isTop?k:-1}" ondragstart="tgDragStart(event)">${fmt(val)}</td>`;
    }
    coeffTbl+='</tr>';
  }
  coeffTbl+='</tbody></table></div>';
  let omegaList='';
  for(let k=0;k<TG.n;k++){
    const active=(!done && nextKind==='omega term' && nextK===k)?'omega-item-active':'';
    omegaList+=`<div class="omega-item ${active}" draggable="true" data-kind="omega" data-idx="${k}" ondragstart="tgDragStart(event)">${K(`\\omega_${k}(x)=${tgOmegaValueLatex(k)}`,false)}</div>`;
  }
  const c=document.getElementById('tg-content');
  c.innerHTML=`
<div class="target-box">
  <div class="target-label">Step 3 — Build P(x) From Both Sides</div>
  <div style="font-size:.76rem;color:var(--text2);margin-bottom:8px;">Drag from left (omega terms) and right (table coefficients) into the center in order: coefficient, omega, coefficient, omega...</div>
  <div class="tg-poly-grid">
    <div class="tg-poly-left">
      <div class="target-label">Omega terms</div>
      ${omegaList}
    </div>
    <div class="tg-poly-mid">
      <div class="tg-drop-zone ${done?'done':''}" ondragover="tgAllowDrop(event)" ondrop="tgDrop(event,'poly')">${done?'Polynomial sequence complete':`Drop ${nextKind} #${nextK} here`}</div>
      <div style="margin-top:10px;font-size:.9rem;overflow-x:auto;">${built?K(`P(x)= ${built}`,false):'P(x)= ?'}</div>
    </div>
    <div class="tg-poly-right">
      <div class="target-label">From full table</div>
      ${coeffTbl}
    </div>
  </div>
</div>
<div class="fb" id="tg-fb"></div>
<div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
  <button class="btn btn-secondary" onclick="tgNewRound()">Restart</button>
</div>`;
}
function tgRenderDone(){
  const finalTex=`P(x)=${Array.from({length:TG.n},(_,k)=>`${tgCoeffLatex(k)}\\,${tgOmegaValueLatex(k)}`).join(' ')}`;
  const c=document.getElementById('tg-content');
  c.innerHTML=`
<div class="target-box">
  <div class="target-label">Tutorial Complete</div>
  <div style="font-size:.9rem;overflow-x:auto;margin:8px 0;">${K(finalTex,false)}</div>
  <div style="font-family:var(--mono);font-size:.76rem;color:var(--text2);margin-bottom:10px;">Great job. Now try a prediction by choosing an x-value.</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
    <input id="tg-pred-x" class="typed-field" type="text" inputmode="decimal" placeholder="x value">
    <button class="btn btn-primary" onclick="tgPredict()">Predict P(x)</button>
    <span id="tg-pred-out" style="font-family:var(--mono);font-size:.76rem;color:var(--accent);"></span>
  </div>
</div>
<div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
  <button class="btn btn-primary" onclick="tgNewRound()">Restart from Step 1</button>
  <button class="btn btn-secondary" onclick="tgNewRound()">Try Again</button>
</div>`;
}
function tgPredict(){
  const xEl=document.getElementById('tg-pred-x');
  const out=document.getElementById('tg-pred-out');
  if(!xEl||!out) return;
  const x=parseFloat(xEl.value);
  if(Number.isNaN(x)){ out.textContent='Enter a valid x.'; return; }
  const y=r4(evalNewton(TG.pts,TG.t,x));
  out.textContent=`P(${fmt(x)}) = ${fmt(y)}`;
}
function tgRender(){
  if(TG.phase==='terms') return tgRenderTerms();
  if(TG.phase==='table') return tgRenderTable();
  if(TG.phase==='poly') return tgRenderPoly();
  return tgRenderDone();
}
function tgPick(val){
  if(TG.phase!=='table') return;
  const {cv,step,ci,cj,t}=TG;
  const slotOrder=['nt','nb','xt','xb'];
  const expSlot=slotOrder[step];
  if(val===expSlot){
    TG.sel.push(cv[step]); TG.step++; TG.ok++;
    showFB('tg-fb',`Slot ${TG.step} correct.`,'ok');
    if(TG.step===4){
      TG.rev[ci][cj]=true; TG.sel=[]; TG.step=0;
      showFB('tg-fb',`Cell solved. Value = ${fmt(r4(t[ci][cj]))}`,'ok');
      setTimeout(tgAdvanceTarget,850);
    } else setTimeout(tgRender,320);
  } else {
    showFB('tg-fb',`Wrong source cell for slot ${step+1}.`,'err');
    doShake('tg-content');
    setTimeout(tgRender,550);
  }
}
function tgPolyRender(){
  if(TG.phase!=='table') return;
  const {pts,t,n,rev}=TG;
  const el=document.getElementById('tg-poly'); if(!el) return;
  let tex='P(x)=', bTex='', hasMore=false;
  for(let k=0;k<n;k++){
    if(k>0&&!rev[0][k]) break;
    const c=r4(t[0][k]);
    if(k===0){tex+=fmt(c);}
    else{
      const xk=pts[k-1].x, sg=xk>=0?'-':'+', ax=fmt(Math.abs(xk));
      bTex+=`(x ${sg} ${ax})`;
      const s2=c>=0?'+':'-';
      tex+=` ${s2} ${fmt(Math.abs(c))}\\,${bTex}`;
      hasMore=true;
    }
  }
  el.innerHTML=K(tex,false);
}

// ─────────────────────────────────────────────
// ADVANCED GAME
// ─────────────────────────────────────────────
let advLevel=1, _advTimer=null, ADV={};
function pickLv(l){
  advLevel=l;
  document.querySelectorAll('.lv-card').forEach(c=>c.classList.remove('active'));
  document.getElementById('lc'+l).classList.add('active');
}
function advReset(){
  clearInterval(_advTimer);
  document.getElementById('adv-start-area').style.display='block';
  document.getElementById('adv-game').style.display='none';
}
function advStart(){
  document.getElementById('adv-start-area').style.display='none';
  document.getElementById('adv-game').style.display='block';
  advNewRound(true);
}
function advNewRound(fresh){
  clearInterval(_advTimer);
  const n=advLevel===1?4:3;
  const pts=genPoints(n), t=ddTable(pts);
  const rev=Array.from({length:n},()=>new Array(n).fill(false));
  for(let i=0;i<n;i++) rev[i][0]=true;
  ADV={level:advLevel,pts,t,n,rev,ci:0,cj:1,step:0,sel:[],
    ok:0,err:0,hearts:3,timeLeft:60,total:60,
    round:fresh?1:(ADV.round||0)+1,cv:[]};
  advRender();
  _advTimer=setInterval(()=>{
    ADV.timeLeft--; advTimerTick();
    if(ADV.timeLeft<=0){clearInterval(_advTimer);advTimeUp();}
  },1000);
}
function advTimerTick(){
  const b=document.getElementById('adv-tbar'), l=document.getElementById('adv-tlbl');
  if(!b||!l) return;
  const p=(ADV.timeLeft/ADV.total)*100;
  b.style.width=p+'%'; b.className='timer-bar'+(p<30?' warn':'');
  l.textContent=ADV.timeLeft+'s';
}
function advTimeUp(){
  showResult({emoji:'',title:"Time's Up!",sub:`You had ${ADV.hearts} heart(s) remaining.`,
    ok:ADV.ok,err:ADV.err,time:ADV.total+'s',score:ADV.ok*10-ADV.err*5,
    btns:[{lbl:'Try Again',fn:'advNewRound(true);hideResult()'},{lbl:'Back to Levels',fn:'advReset();hideResult()'}]
  });
}
function advRender(){
  const {pts,t,n,rev,ci,cj,step,sel,hearts,ok,err,level,round}=ADV;
  const cv=level===1
    ? [r4(t[ci+1][cj-1]),r4(t[ci][cj-1]),r4(pts[ci+cj].x),r4(pts[ci].x)]
    : [r4(t[ci+1][cj-1]),r4(t[ci][cj-1]),r4(pts[ci+cj].x-pts[ci].x)];
  ADV.cv=cv;
  const slots=level===1?{
    nt:{row:ci+cj,col:cj-1,val:cv[0],label:'numerator top'},
    nb:{row:ci+cj-1,col:cj-1,val:cv[1],label:'numerator bottom'},
    xt:{row:ci+cj,col:'x',val:cv[2],label:'x top'},
    xb:{row:ci,col:'x',val:cv[3],label:'x bottom'}
  }:null;
  const pool=new Set();
  for(let i=0;i<n;i++) for(let j=0;j<n;j++) if(i+j<n) pool.add(r4(t[i][j]));
  for(let i=0;i<n;i++) pool.add(pts[i].x);
  for(let i=0;i<n-1;i++) pool.add(pts[i+1].x-pts[i].x);
  const poolArr=[...pool].sort(()=>Math.random()-.5);

  const liveFml=()=>{
    const token=(k)=>{
      if(k<sel.length) return fmt(sel[k]);
      if(k===step) return '<span class="hot">?</span>';
      return '?';
    };
    return `<span class="frac"><span class="num">(${token(0)})-(${token(1)})</span><span class="den">(${token(2)})-(${token(3)})</span></span>`;
  };
  let tbl='<div class="dd-wrap"><table class="dd-table"><thead><tr><th>x</th><th>f[x]</th>';
  for(let j=1;j<n;j++) tbl+=`<th>Ord.${j}</th>`;
  tbl+='</tr></thead><tbody>';
  for(let i=0;i<n;i++){
    const xToken=(level===1&&step===2&&i===slots.xt.row)?'xt':(level===1&&step===3&&i===slots.xb.row)?'xb':'';
    tbl+=`<tr><td class="cell-known ${xToken?'cell-source':''}" style="font-size:.72rem;" ${xToken?`onclick="advPick('${xToken}')"`:''}>${fmt(pts[i].x)}</td>`;
    for(let j=0;j<n;j++){
      if(j===0){
        const yToken=(level===1&&cj-1===0&&step===0&&i===slots.nt.row)?'nt':(level===1&&cj-1===0&&step===1&&i===slots.nb.row)?'nb':'';
        tbl+=`<td class="cell-known ${yToken?'cell-source':''}" ${yToken?`onclick="advPick('${yToken}')"`:''}>${fmt(t[i][0])}</td>`;
        continue;
      }
      if(i<j){tbl+='<td class="cell-empty"></td>';continue;}
      const ti=i-j;
      const ddToken=(level===1&&j===cj-1&&step===0&&i===slots.nt.row)?'nt':(level===1&&j===cj-1&&step===1&&i===slots.nb.row)?'nb':'';
      if(rev[ti][j]){
        const a=fmt(r4(t[ti+1][j-1])), b=fmt(r4(t[ti][j-1])), c=fmt(r4(pts[ti+j].x)), d=fmt(r4(pts[ti].x));
        tbl+=`<td class="cell-revealed ${ddToken?'cell-source':''}" ${ddToken?`onclick="advPick('${ddToken}')"`:''}>${fmt(r4(t[ti][j]))}<div class="cell-note"><span class="frac"><span class="num">(${a})-(${b})</span><span class="den">(${c})-(${d})</span></span></div></td>`;
      }
      else if(ti===ci&&j===cj){
        if(level===1){
          const slotOrder=['nt','nb','xt','xb'];
          tbl+=`<td class="cell-target"><div class="cell-live-formula">${liveFml()}</div><div class="cell-prompt">Click source cell for: ${slots[slotOrder[step]].label}</div></td>`;
        } else {
          tbl+=`<td class="cell-target">← NOW</td>`;
        }
      }
      else tbl+=`<td class="cell-hidden" style="font-size:.65rem;">hidden</td>`;
    }
    tbl+='</tr>';
  }
  tbl+='</tbody></table></div>';

  const slotBtns=[0,1,2].map(s=>{
    if(s<sel.length) return `<button class="op-btn selected" disabled>${fmt(sel[s])}<span class="slot-pill">S${s+1}</span></button>`;
    if(s===step) return `<button class="op-btn" style="border-color:var(--blue);color:var(--blue);" disabled>→<span class="slot-pill">S${s+1}</span></button>`;
    return `<button class="op-btn" style="opacity:.2;" disabled><span class="slot-pill">S${s+1}</span></button>`;
  }).join('');

  let inputSection='';
  if(level===2){
    inputSection=`<div class="typed-row">
      ${[0,1,2].map(s=>`<div style="text-align:center;"><div style="font-family:var(--mono);font-size:.58rem;color:var(--text3);margin-bottom:3px;">Slot ${s+1}</div><input class="typed-field" id="adv-t${s}" type="number" step="any" placeholder="S${s+1}" onkeydown="if(event.key==='Enter')advSubmit()"></div>`).join('')}
      <button class="btn btn-primary" onclick="advSubmit()" style="padding:8px 13px;align-self:flex-end;">Submit</button>
    </div>`;
  }

  const fTex=level===1
    ? `\\dfrac{${fmt(r4(t[ci+1][cj-1]))}-(${fmt(r4(t[ci][cj-1]))})}{${fmt(pts[ci+cj].x)}-${fmt(pts[ci].x)}}`
    : `\\dfrac{${fmt(r4(t[ci+1][cj-1]))}-(${fmt(r4(t[ci][cj-1]))})}{${fmt(pts[ci+cj].x-pts[ci].x)}}`;
  const g=document.getElementById('adv-game');
  g.innerHTML=`
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:7px;">
  <div style="font-family:var(--mono);font-size:.82rem;color:var(--accent);">L${level} · Round ${round}</div>
  <div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;">
    <span style="font-family:var(--mono);font-size:.76rem;color:var(--text2);">Correct ${ok} Mistakes ${err}</span>
    <span style="font-family:var(--mono);font-size:.95rem;color:var(--red);">Hearts ${hearts}/3</span>
    <span id="adv-tlbl" style="font-family:var(--mono);font-size:.9rem;color:var(--accent);font-weight:700;"></span>
  </div>
</div>
<div class="timer-wrap"><div class="timer-bar" id="adv-tbar" style="width:100%;"></div></div>
${tbl}
<div class="target-box" style="margin-top:10px;">
  <div class="target-label">Target — row ${ci+cj}, order ${cj}</div>
  <div id="adv-fml" style="font-size:.88rem;overflow-x:auto;margin:6px 0;"></div>
  <div style="font-size:.72rem;color:var(--blue);">${level===1?'Click values inside the highlighted table cell.':`Fill Slot ${step+1}`}</div>
</div>
${level===2?`<div style="display:flex;gap:7px;flex-wrap:wrap;margin:8px 0;">${slotBtns}</div>`:''}
${inputSection}
<div class="fb" id="adv-fb"></div>
<div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;">
  <button class="btn btn-secondary" onclick="advNewRound(false)">New Round</button>
  <button class="btn-back" onclick="clearInterval(_advTimer);advReset()" style="padding:9px 14px;">← Levels</button>
</div>`;
  const fEl=document.getElementById('adv-fml');
  if(fEl) fEl.innerHTML=K(fTex,false);
  advTimerTick();
  if(level===2) setTimeout(()=>document.getElementById('adv-t0')?.focus(),60);
}
function advPick(val){
  const {cv,step,ci,cj,t}=ADV;
  const slotOrder=['nt','nb','xt','xb'];
  const expSlot=slotOrder[step];
  if(val===expSlot){
    ADV.sel.push(cv[step]); ADV.step++; ADV.ok++;
    showFB('adv-fb',`Slot ${ADV.step} correct.`,'ok');
    if(ADV.step===4) advSolveCell();
    else setTimeout(advRender,280);
  } else advWrong();
}
function advSubmit(){
  const {cv}=ADV; let allOk=true; const vals=[];
  for(let s=0;s<3;s++){
    const el=document.getElementById(`adv-t${s}`); if(!el) return;
    const got=r4(parseFloat(el.value)), exp=r4(cv[s]);
    vals.push(got);
    if(Math.abs(got-exp)>0.0001){el.classList.add('err');allOk=false;}
    else el.classList.add('ok');
  }
  if(allOk){ADV.ok+=3;ADV.sel=vals;ADV.step=3;showFB('adv-fb','All slots correct.','ok');setTimeout(advSolveCell,480);}
  else advWrong();
}
function advSolveCell(){
  ADV.rev[ADV.ci][ADV.cj]=true; ADV.sel=[]; ADV.step=0;
  let {ci,cj,n}=ADV; ci++; if(ci>n-cj-1){cj++;ci=0;}
  if(cj>=n){clearInterval(_advTimer);advRoundDone();return;}
  ADV.ci=ci; ADV.cj=cj; advRender();
}
function advWrong(){
  ADV.err++; ADV.hearts--;
  showFB('adv-fb','Wrong. -1 heart.','err'); doShake('adv-game');
  if(ADV.hearts<=0){
    clearInterval(_advTimer);
    showResult({emoji:'',title:'No Hearts Left!',sub:'Try again.',
      ok:ADV.ok,err:ADV.err,time:(ADV.total-ADV.timeLeft)+'s',score:ADV.ok*10-ADV.err*5,
      btns:[{lbl:'Try Again',fn:'advNewRound(true);hideResult()'},{lbl:'Back to Levels',fn:'advReset();hideResult()'}]
    });return;
  }
  setTimeout(advRender,480);
}
function advRoundDone(){
  const {ok,err,hearts,total,timeLeft,round,level}=ADV;
  showResult({emoji:'',title:'Round Complete!',sub:`L${level} solved in ${total-timeLeft}s with ${hearts} hearts left.`,
    ok,err,time:(total-timeLeft)+'s',score:ok*10-err*5+hearts*15,
    btns:[{lbl:'Next Round',fn:'advNewRound(false);hideResult()'},{lbl:'Back to Levels',fn:'advReset();hideResult()'}]
  });
}

// ─────────────────────────────────────────────
// VISUALIZATION LAB
// ─────────────────────────────────────────────
let VIZ_PTS=[], _chart=null, VIZ_ORD=0;
function vizInit(){
  VIZ_PTS=[{x:-2,y:3},{x:0,y:-1},{x:1,y:2},{x:3,y:5}];
  VIZ_ORD=0;
  const canvas=document.getElementById('viz-canvas');
  _chart=new Chart(canvas,{
    type:'line',data:{datasets:[]},
    options:{responsive:true,maintainAspectRatio:true,animation:{duration:350},
      plugins:{legend:{labels:{color:'#a0a0b4',font:{family:'JetBrains Mono',size:11},usePointStyle:true,pointStyleWidth:28}}},
      scales:{
        x:{type:'linear',ticks:{color:'#606078',font:{family:'JetBrains Mono',size:10}},grid:{color:'#2a2a32'}},
        y:{ticks:{color:'#606078',font:{family:'JetBrains Mono',size:10}},grid:{color:'#2a2a32'}}
      }
    }
  });
  vizRender();
}
function vizRender(){
  const pts=[...VIZ_PTS].sort((a,b)=>a.x-b.x);
  // point list
  document.getElementById('viz-list').innerHTML=VIZ_PTS.length?VIZ_PTS.map((p,i)=>`<div class="point-row"><div class="point-coord">(${fmt(p.x)}, ${fmt(p.y)})</div><button class="btn-rm" onclick="vizDel(${i})">x</button></div>`).join(''):'<div style="color:var(--text3);font-family:var(--mono);font-size:.78rem;">No points yet.</div>';

  if(pts.length<1){
    document.getElementById('viz-poly').textContent='Add ≥ 1 point.';
    document.getElementById('viz-ord-label').textContent='Order: —';
    document.getElementById('viz-prev').disabled=true;
    document.getElementById('viz-next').disabled=true;
    document.getElementById('viz-dd').innerHTML='';
    if(_chart){_chart.data.datasets=[];_chart.update();}
    return;
  }
  const t=ddTable(pts);
  const ordMax=pts.length-1;
  VIZ_ORD=Math.max(0,Math.min(ordMax,VIZ_ORD));
  const pTex=polyLatexOrd(pts,t,VIZ_ORD);
  document.getElementById('viz-poly').innerHTML=K(pTex,false);
  document.getElementById('viz-ord-label').textContent=`Order: ORD${VIZ_ORD} / ORD${ordMax}`;
  document.getElementById('viz-prev').disabled=(VIZ_ORD<=0);
  document.getElementById('viz-next').disabled=(VIZ_ORD>=ordMax);

  // curve
  const xs=pts.map(p=>p.x);
  const ys=pts.map(p=>p.y);
  const xMin=Math.min(...xs)-1.5, xMax=Math.max(...xs)+1.5;
  const curveData=[];
  const curveSamples=220;
  for(let i=0;i<=curveSamples;i++){
    const x=xMin+((xMax-xMin)*i/curveSamples);
    curveData.push({x,y:evalNewtonOrd(pts,t,x,VIZ_ORD)});
  }

  if(_chart){
    // Keep the viewport anchored to the raw points so changing order
    // does not visually move the points due to axis auto-rescaling.
    const pxMin=Math.min(...xs), pxMax=Math.max(...xs);
    const pyMin=Math.min(...ys), pyMax=Math.max(...ys);
    const xPad=Math.max(0.8,(pxMax-pxMin)*0.2);
    const yPad=Math.max(0.8,(pyMax-pyMin)*0.2);
    _chart.options.scales.x.min=pxMin-xPad;
    _chart.options.scales.x.max=pxMax+xPad;
    _chart.options.scales.y.min=pyMin-yPad;
    _chart.options.scales.y.max=pyMax+yPad;
    if(!_chart.data.datasets.length){
      _chart.data.datasets=[
        {label:`P(x) @ ORD${VIZ_ORD}`,data:curveData,borderColor:'#e2b714',backgroundColor:'#e2b714',pointStyle:'line',pointRadius:0,pointHoverRadius:0,pointHitRadius:0,pointBorderWidth:0,borderWidth:3,tension:0.1,fill:false},
        {label:'Points',data:pts.map(p=>({x:p.x,y:p.y})),borderColor:'#4ade80',backgroundColor:'#4ade80',pointStyle:'circle',pointRadius:4,pointHoverRadius:6,showLine:false,animation:false,order:99}
      ];
    }else{
      _chart.data.datasets[0].label=`P(x) @ ORD${VIZ_ORD}`;
      _chart.data.datasets[0].data=curveData;
      _chart.data.datasets[1].data=pts.map(p=>({x:p.x,y:p.y}));
    }
    _chart.update();
  }

  // DD table
  const n=pts.length;
  let ddh='<div style="margin-top:12px;font-family:var(--mono);font-size:.62rem;color:var(--text3);letter-spacing:.15em;text-transform:uppercase;margin-bottom:8px;">Divided Difference Table</div><div class="dd-wrap"><table class="dd-table"><thead><tr><th>x</th><th>f[x]</th>';
  for(let j=1;j<n;j++) ddh+=`<th>Ord.${j}</th>`;
  ddh+='</tr></thead><tbody>';
  for(let i=0;i<n;i++){
    ddh+=`<tr><td class="cell-known">${fmt(pts[i].x)}</td>`;
    for(let j=0;j<n;j++){
      if(j===0){ddh+=`<td class="cell-known">${fmt(r4(t[i][0]))}</td>`;continue;}
      if(i<j){ddh+='<td class="cell-empty"></td>';continue;}
      const ti=i-j;
      ddh+=`<td class="cell-revealed">${fmt(r4(t[ti][j]))}</td>`;
    }
    ddh+='</tr>';
  }
  ddh+='</tbody></table></div>';
  document.getElementById('viz-dd').innerHTML=ddh;
}
function vizAdd(){
  const x=parseFloat(document.getElementById('vx').value), y=parseFloat(document.getElementById('vy').value);
  if(isNaN(x)||isNaN(y)) return;
  if(VIZ_PTS.some(p=>p.x===x)){alert('x must be unique!');return;}
  VIZ_PTS.push({x,y});
  VIZ_ORD=0;
  document.getElementById('vx').value=''; document.getElementById('vy').value='';
  vizRender();
}
function vizDel(i){VIZ_PTS.splice(i,1);VIZ_ORD=Math.max(0,Math.min(VIZ_ORD,VIZ_PTS.length-1));vizRender();}
function vizRandom(){VIZ_PTS=genPoints(rnd(3,5),-4,4);VIZ_ORD=0;vizRender();}
function vizClear(){VIZ_PTS=[];VIZ_ORD=0;vizRender();}
function vizStep(d){
  VIZ_ORD=Math.max(0,VIZ_ORD+d);
  vizRender();
}

// ─────────────────────────────────────────────
// CHALLENGE MODE
// ─────────────────────────────────────────────
let _chTimer=null, CH={};
function chFactorStr(x){
  const xv=r4(x);
  return xv>=0?`(x-${fmt(xv)})`:`(x+${fmt(Math.abs(xv))})`;
}
function chOmegaStr(k){
  if(k===0) return '1';
  let out='';
  for(let i=0;i<k;i++) out+=chFactorStr(CH.pts[i].x);
  return out;
}
function chOmegaLatexWithPicks(k,picks){
  if(k===0) return '\\omega_0(x)=1';
  let out=`\\omega_${k}(x)=`;
  for(let i=0;i<k;i++){
    if(i<picks.length) out+=chFactorStr(CH.pts[picks[i]].x);
    else out+='(x-\\color{orange}{?})';
  }
  return out;
}
function chLoseLife(msg){
  CH.err++; CH.hearts--;
  showFB('ch-fb',msg||'Wrong. -1 heart.','err');
  doShake('ch-game');
  if(CH.hearts<=0){
    clearInterval(_chTimer);
    showResult({emoji:'',title:'Game Over',sub:'No hearts left.',
      ok:CH.ok,err:CH.err,time:'—',score:'—',
      btns:[{lbl:'Play Again',fn:'CH={hearts:3};chBegin();hideResult()'},{lbl:'Back to Menu',fn:'go("menu");hideResult()'}]
    });
    return true;
  }
  return false;
}
function chReset(){
  clearInterval(_chTimer);
  document.getElementById('ch-start-area').style.display='block';
  document.getElementById('ch-game').style.display='none';
  CH={hearts:3,mode:'solo'};
}
function chBegin(){
  document.getElementById('ch-start-area').style.display='none';
  document.getElementById('ch-game').style.display='block';
  chNewRound({mode:'solo',total:80});
}
function chNewRound(opts={}){
  clearInterval(_chTimer);
  const pts=opts.forcedPts||genPoints(4), t=ddTable(pts), n=4;
  const rev=Array.from({length:n},()=>new Array(n).fill(false));
  for(let i=0;i<n;i++) rev[i][0]=true;
  const total=opts.total||80;
  Object.assign(CH,{
    pts,t,n,rev,ci:0,cj:1,step:0,sel:[],
    ok:0,err:0,timeLeft:total,total,mode:'solo',
    termsStep:1,termsPick:[],termsDone:false,
    tableDone:false,
    polyTokenStep:0,polyTokens:[]
  });
  chRender();
  _chTimer=setInterval(()=>{
    CH.timeLeft--; chTimerTick();
    if(CH.timeLeft<=0){clearInterval(_chTimer);chTimeUp();}
  },1000);
}
function chTimerTick(){
  const b=document.getElementById('ch-tbar'), l=document.getElementById('ch-tlbl');
  if(!b||!l) return;
  const p=(CH.timeLeft/CH.total)*100;
  b.style.width=p+'%'; b.className='timer-bar'+(p<40?' warn':'');
  l.textContent=CH.timeLeft+'s';
}
function chTimeUp(){
  showResult({emoji:'',title:"Time's Up!",sub:`Hearts left: ${Math.max(0,CH.hearts)}`,
    ok:CH.ok,err:CH.err,time:CH.total+'s',score:'—',
    btns:[{lbl:'Try Again',fn:'chNewRound();hideResult()'},{lbl:'Back to Menu',fn:'go("menu");hideResult()'}]
  });
}
function chTableExpected(){
  const {ci,cj,pts,t}=CH;
  return [r4(t[ci+1][cj-1]),r4(t[ci][cj-1]),r4(pts[ci+cj].x),r4(pts[ci].x)];
}
function chAdvanceTable(){
  let {ci,cj,n}=CH;
  ci++; if(ci>n-cj-1){cj++;ci=0;}
  if(cj>=n){CH.tableDone=true; return;}
  CH.ci=ci; CH.cj=cj; CH.step=0; CH.sel=[];
}
function chFocusActiveInput(){
  if(CH.phase==='over') return;
  let el=null;
  if((CH.termsStep||0)<CH.n) el=document.getElementById('ch-term-input');
  else if(!CH.tableDone) el=document.getElementById('ch-table-input');
  else if((CH.polyTokenStep||0)<CH.n*2) el=document.getElementById('ch-poly-input');
  else el=document.getElementById('ch-pred-input');
  if(el){
    el.focus();
    el.select?.();
  }
}
function chRender(){
  const heartCount=Math.max(0,Math.min(3,CH.hearts||0));
  const heartsLive='💛'.repeat(heartCount);
  const heartsLost='🤍'.repeat(3-heartCount);
  const heartsMarkup=`${heartsLive}${heartsLost}`;
  const {pts,t,n,rev,ci,cj,ok,err,step}=CH;
  const termsDone=CH.termsStep>=n;
  const tableDone=CH.tableDone;
  const polyDone=(CH.polyTokenStep||0)>=n*2;

  let termsRows=Array.from({length:n},(_,k)=>{
    if(k===0) return '\\omega_0(x)=1';
    if(k<CH.termsStep) return `\\omega_${k}(x)=${chOmegaStr(k)}`;
    if(k===CH.termsStep&&!termsDone) return chOmegaLatexWithPicks(k,CH.termsPick||[]);
    return chOmegaLatexWithPicks(k,[]);
  }).map((r,k)=>`<div class="omega-row ${(!termsDone&&k===CH.termsStep)?'omega-row-active':''}">${K(r,false)}</div>`).join('');
  let ptsTbl='<div class="dd-wrap"><table class="dd-table tg-pts-table" style="min-width:280px;"><thead><tr><th class="tg-idx-sm">i</th><th>x</th><th>y</th></tr></thead><tbody>';
  for(let i=0;i<n;i++) ptsTbl+=`<tr><td class="cell-index tg-idx-sm">${i}</td><td class="cell-known">${fmt(pts[i].x)}</td><td class="cell-known">${fmt(pts[i].y)}</td></tr>`;
  ptsTbl+='</tbody></table></div>';

  let tbl='<div class="dd-wrap"><table class="dd-table"><thead><tr><th>x</th><th>f[x]</th>';
  for(let j=1;j<n;j++) tbl+=`<th>Ord.${j}</th>`;
  tbl+='</tr></thead><tbody>';
  for(let i=0;i<n;i++){
    tbl+=`<tr><td class="cell-known" style="font-size:.72rem;">${fmt(pts[i].x)}</td>`;
    for(let j=0;j<n;j++){
      if(j===0){tbl+=`<td class="cell-known">${fmt(t[i][0])}</td>`;continue;}
      if(i<j){tbl+='<td class="cell-empty"></td>';continue;}
      const ti=i-j;
      if(rev[ti][j]){
        const a=fmt(r4(t[ti+1][j-1])), b=fmt(r4(t[ti][j-1])), c=fmt(r4(pts[ti+j].x)), d=fmt(r4(pts[ti].x));
        tbl+=`<td class="cell-revealed">${fmt(r4(t[ti][j]))}<div class="cell-note"><span class="frac"><span class="num">(${a})-(${b})</span><span class="den">(${c})-(${d})</span></span></div></td>`;
      } else if(ti===ci&&j===cj){
        const tok=(k)=>k<CH.sel.length?fmt(CH.sel[k]):k===CH.step?'<span class="hot">?</span>':'?';
        const live=`<span class="frac"><span class="num">(${tok(0)})-(${tok(1)})</span><span class="den">(${tok(2)})-(${tok(3)})</span></span>`;
        tbl+=`<td class="cell-target"><div class="cell-live-formula">${live}</div><div class="cell-prompt">Type value for slot ${step+1}</div></td>`;
      }
      else tbl+=`<td class="cell-hidden" style="font-size:.65rem;">hidden</td>`;
    }
    tbl+='</tr>';
  }
  tbl+='</tbody></table></div>';

  const s=CH.polyTokenStep||0, k=Math.floor(s/2);
  const wantCoeff=(s%2===0);
  const polyBuilt=(CH.polyTokens||[]).join('\\,');
  const g=document.getElementById('ch-game');
  g.innerHTML=`
<div style="display:flex;justify-content:space-between;margin-bottom:8px;flex-wrap:wrap;gap:6px;">
  <span style="font-family:var(--mono);font-size:.78rem;color:var(--text2);">Correct ${ok} Mistakes ${err}</span>
  <span id="ch-tlbl" style="font-family:var(--mono);font-size:.95rem;color:var(--accent);font-weight:700;"></span>
</div>
<div class="timer-wrap"><div class="timer-bar" id="ch-tbar" style="width:100%;"></div></div>
<div class="ch-lives-wrap">
  <span class="ch-lives-label">Lives</span>
  <span class="ch-lives-hearts">${heartsMarkup}</span>
</div>
<div class="ch-grid2-top">
  <div class="target-box ${termsDone?'ch-done-panel':''}">
    <div class="target-label">Terms (typed)</div>
    ${ptsTbl}
    <div class="omega-tri">${termsRows}</div>
    ${termsDone?`<div style="font-size:.74rem;color:var(--green);margin-top:8px;">Done</div>`:`
    <div class="typed-row" style="margin-top:10px;">
      <input id="ch-term-input" class="typed-field" type="text" inputmode="decimal" placeholder="next x for ω${CH.termsStep}" onkeydown="if(event.key==='Enter')chSubmitTerm()">
      <button class="btn btn-primary" onclick="chSubmitTerm()">OK</button>
    </div>
    <div style="font-size:.7rem;color:var(--text2);">Type x-value in order for current omega row.</div>`}
  </div>
  <div class="target-box ${(!termsDone)?'ch-locked-panel':tableDone?'ch-done-panel':''}">
    <div class="target-label">Table (typed)</div>
    ${tbl}
    ${tableDone?`<div style="font-size:.74rem;color:var(--green);margin-top:8px;">Done</div>`:termsDone?`
    <div class="typed-row" style="margin-top:10px;">
      <input id="ch-table-input" class="typed-field" type="text" inputmode="decimal" placeholder="slot ${step+1}" onkeydown="if(event.key==='Enter')chSubmitTable()">
      <button class="btn btn-primary" onclick="chSubmitTable()">OK</button>
    </div>
    <div style="font-size:.7rem;color:var(--text2);">Target row ${ci+cj}, order ${cj}.</div>`:`<div style="font-size:.7rem;color:var(--text3);margin-top:8px;">Complete Terms first.</div>`}
  </div>
  </div>
</div>
<div class="ch-grid-bottom">
  <div class="target-box ${(!tableDone)?'ch-locked-panel':polyDone?'ch-done-panel':''}">
    <div class="target-label">Polynomial (typed)</div>
    <div style="font-size:.74rem;color:var(--text2);margin-bottom:8px;">Type alternating: coefficient then omega term.</div>
    <div style="font-size:.9rem;overflow-x:auto;margin-bottom:8px;">${polyBuilt?K(`P(x)= ${polyBuilt}`,false):'P(x)= ?'}</div>
    ${polyDone?`
      <div class="typed-row">
        <input id="ch-pred-input" class="typed-field" type="text" inputmode="decimal" placeholder="x value" onkeydown="if(event.key==='Enter')chPredictSolo()">
        <button class="btn btn-primary" onclick="chPredictSolo()">Predict</button>
      </div>
      <div id="ch-pred-out" style="font-size:.75rem;color:var(--accent);font-family:var(--mono);"></div>
      <button class="btn btn-secondary" onclick="chNewRound()" style="margin-top:10px;">Restart from step 1</button>
    `:tableDone?`
    <div class="typed-row">
      <input id="ch-poly-input" class="typed-field" type="text" placeholder="${wantCoeff?`a${k} value`:`ω${k}(x) term`}" onkeydown="if(event.key==='Enter')chSubmitPoly()">
      <button class="btn btn-primary" onclick="chSubmitPoly()">OK</button>
    </div>
    <div style="font-size:.7rem;color:var(--text2);">Now type ${wantCoeff?`coefficient a${k}`:`omega term ω${k}(x)`}.</div>`:`<div style="font-size:.7rem;color:var(--text3);margin-top:8px;">Complete Table first.</div>`}
  </div>
</div>
<div class="fb" id="ch-fb"></div>
<div style="margin-top:10px;display:flex;gap:8px;">
  <button class="btn btn-secondary" onclick="chNewRound()">Restart</button>
</div>`;
  chTimerTick();
  setTimeout(chFocusActiveInput,30);
}
function chSubmitTerm(){
  if(CH.termsStep>=CH.n) return;
  const el=document.getElementById('ch-term-input'); if(!el) return;
  const v=parseFloat(el.value.trim());
  if(Number.isNaN(v)){ if(!chLoseLife('Type a number.')) chRender(); return; }
  const expIdx=(CH.termsPick||[]).length;
  const exp=r4(CH.pts[expIdx].x);
  if(Math.abs(r4(v)-exp)>0.0001){ if(!chLoseLife(`Expected x${expIdx} first.`)) chRender(); return; }
  CH.termsPick.push(expIdx); CH.ok++;
  if(CH.termsPick.length===CH.termsStep){
    CH.termsStep++; CH.termsPick=[];
    showFB('ch-fb',`ω${CH.termsStep-1} completed.`,'ok');
  }
  chRender();
}
function chSubmitTable(){
  if(CH.tableDone || CH.termsStep<CH.n) return;
  const el=document.getElementById('ch-table-input'); if(!el) return;
  const v=parseFloat(el.value.trim());
  if(Number.isNaN(v)){ if(!chLoseLife('Type a number.')) chRender(); return; }
  const exp=chTableExpected()[CH.step];
  if(Math.abs(r4(v)-exp)>0.0001){ if(!chLoseLife('Wrong table slot value.')) chRender(); return; }
  CH.sel.push(exp); CH.step++; CH.ok++;
  if(CH.step===4){
    CH.rev[CH.ci][CH.cj]=true;
    chAdvanceTable();
  }
  chRender();
}
function chNormExpr(s){ return (s||'').toLowerCase().replace(/\s+/g,''); }
function chSubmitPoly(){
  if(!CH.tableDone) return;
  const done=(CH.polyTokenStep||0)>=CH.n*2; if(done) return;
  const el=document.getElementById('ch-poly-input'); if(!el) return;
  const raw=el.value.trim();
  const s=CH.polyTokenStep||0, k=Math.floor(s/2), wantCoeff=(s%2===0);
  if(wantCoeff){
    const v=parseFloat(raw);
    const exp=r4(CH.t[0][k]);
    if(Number.isNaN(v)||Math.abs(r4(v)-exp)>0.0001){ if(!chLoseLife(`Wrong a${k}.`)) chRender(); return; }
    CH.polyTokens.push(`${k===0?'':exp>=0?'+':'-'}${k===0?fmt(exp):'\\,'+fmt(Math.abs(exp))}`);
  } else {
    const exp=chNormExpr(chOmegaStr(k));
    if(chNormExpr(raw)!==exp){ if(!chLoseLife(`Wrong ω${k}(x) term.`)) chRender(); return; }
    CH.polyTokens.push(chOmegaStr(k));
  }
  CH.ok++; CH.polyTokenStep++;
  chRender();
}
function chPredictSolo(){
  const inEl=document.getElementById('ch-pred-input');
  const out=document.getElementById('ch-pred-out');
  if(!inEl||!out) return;
  const x=parseFloat(inEl.value.trim());
  if(Number.isNaN(x)){ out.textContent='Enter valid x.'; return; }
  const y=r4(evalNewton(CH.pts,CH.t,x));
  out.textContent=`P(${fmt(x)}) = ${fmt(y)}`;
}
function chSubmit(){ chSubmitTable(); }

themeInit();
