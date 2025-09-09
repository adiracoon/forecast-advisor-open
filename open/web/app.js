async function q(path, init) {
  const r = await fetch(path, init);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}
async function refresh() {
  const data = await q('/forecasts');
  document.getElementById('out').textContent = JSON.stringify(data, null, 2);
}
document.getElementById('add').onclick = async () => {
  await q('/forecasts', {method:'POST', headers:{'content-type':'application/json'},
    body: JSON.stringify({title:'sample', value: Math.random()*10})});
  refresh();
};
refresh();
