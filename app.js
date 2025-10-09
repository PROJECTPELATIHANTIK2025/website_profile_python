// app.js - handles calls to Flask APIs (calculator and converter)
document.addEventListener('DOMContentLoaded', () => {
  const btnCalc = document.getElementById('btn-calc');
  const btnConv = document.getElementById('btn-conv');

  if (btnCalc) {
    btnCalc.addEventListener('click', async () => {
      const a = document.getElementById('calc-a').value || 0;
      const b = document.getElementById('calc-b').value || 0;
      const op = document.getElementById('calc-op').value;
      const resultEl = document.getElementById('calc-result');
      resultEl.textContent = '...';
      try {
        const res = await fetch('/api/calculate', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({a, b, op})
        });
        const data = await res.json();
        if (res.ok) resultEl.textContent = data.result;
        else resultEl.textContent = 'Error: ' + (data.error || res.statusText);
      } catch (e) {
        resultEl.textContent = 'Network error';
      }
    });
  }

  if (btnConv) {
    btnConv.addEventListener('click', async () => {
      const value = document.getElementById('conv-value').value || 0;
      const frm = document.getElementById('conv-from').value;
      const to = document.getElementById('conv-to').value;
      const resultEl = document.getElementById('conv-result');
      resultEl.textContent = '...';
      try {
        const res = await fetch('/api/convert-temp', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({value, from: frm, to})
        });
        const data = await res.json();
        if (res.ok) resultEl.textContent = data.result.toFixed(2);
        else resultEl.textContent = 'Error: ' + (data.error || res.statusText);
      } catch (e) {
        resultEl.textContent = 'Network error';
      }
    });
  }
});
