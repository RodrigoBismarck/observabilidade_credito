document.addEventListener('DOMContentLoaded', function(){
  // Toggle images visibility
  document.querySelectorAll('.toggle-images').forEach(btn => {
document.addEventListener('DOMContentLoaded', function(){
  // Toggle images visibility
  document.querySelectorAll('.toggle-images').forEach(btn => {
    btn.addEventListener('click', ()=>{
      document.addEventListener('DOMContentLoaded', function(){
        // Global toggle for images (single control)
        const globalImgBtn = document.getElementById('toggle-images-global');
        if(globalImgBtn){
          globalImgBtn.addEventListener('click', ()=>{
            const imgs = Array.from(document.querySelectorAll('.img-wrap'));
            if(imgs.length===0) return;
            const anyHidden = imgs.some(i=>i.classList.contains('hidden'));
            imgs.forEach(i=>{
              if(anyHidden) i.classList.remove('hidden'); else i.classList.add('hidden');
            });
            globalImgBtn.textContent = anyHidden ? 'Esconder imagens' : 'Mostrar imagens';
          });
        }

        // Simple table sorting
        function sortTable(table, colIndex, numeric){
          const tbody = table.tBodies[0];
          const rows = Array.from(tbody.rows);
          const dir = table.getAttribute('data-sort-dir') === 'asc' ? -1 : 1;
          rows.sort((a,b)=>{
            let av = a.cells[colIndex].textContent.trim();
            let bv = b.cells[colIndex].textContent.trim();
            if(numeric){ av = parseFloat(av)||0; bv = parseFloat(bv)||0; }
            return av > bv ? dir : av < bv ? -dir : 0;
          });
          rows.forEach(r=>tbody.appendChild(r));
          table.setAttribute('data-sort-dir', dir===1? 'asc':'desc');
        }
        document.querySelectorAll('table.sortable thead th').forEach((th, i)=>{
          th.addEventListener('click', ()=>{
            const table = th.closest('table');
            const numeric = th.dataset.numeric === 'true';
            sortTable(table, i, numeric);
          });
        });
      });

      /* small helper: hide images by default via CSS class 'hidden' (handled in styles.css) */

      // show only drifted feature cards, hide others
      function showOnlyDrift(){
        document.querySelectorAll('.card').forEach(c=>{
          if(c.dataset.drift==='true') c.classList.remove('hidden'); else c.classList.add('hidden');
        });
      }

      function showAllCards(){
        document.querySelectorAll('.card').forEach(c=>c.classList.remove('hidden'));
      }

      // toggle full table visibility
      function toggleTable(){
        const t = document.getElementById('all-table-wrap');
        if(!t) return;
        t.classList.toggle('hidden');
      }

      // export visible table rows to CSV
      function exportTableCSV(){
        const table = document.getElementById('drift-table');
        if(!table) return;
        const rows = Array.from(table.tBodies[0].rows);
        const csv = [Array.from(table.tHead.rows[0].cells).map(c=>c.textContent.trim()).join(',')]
          .concat(rows.map(r=>Array.from(r.cells).map(c=>'"'+c.textContent.replace(/"/g,'""')+'"').join(',')) ).join('\n');
        const url = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
        const a = document.createElement('a'); a.href = url; a.download = 'drift_summary.csv'; a.click();
      }

      // expose helpers to global
      window.showOnlyDrift = showOnlyDrift;
      window.showAllCards = showAllCards;
      window.toggleTable = toggleTable;
      window.exportTableCSV = exportTableCSV;
