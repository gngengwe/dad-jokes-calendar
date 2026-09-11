function highlight(i){
  document.querySelectorAll('.pin').forEach((p,idx) => p.classList.toggle('hi', idx===i));
  document.querySelectorAll('.note').forEach(n => n.classList.toggle('hi', Number(n.dataset.idx)===i));
}

document.querySelectorAll('.pin').forEach(pin => {
  const i = Number(pin.dataset.idx);
  pin.addEventListener('mouseenter', () => highlight(i));
  pin.addEventListener('focus', () => highlight(i));
  pin.addEventListener('click', () => highlight(i));
});

document.querySelectorAll('.note').forEach(note => {
  const i = Number(note.dataset.idx);
  note.addEventListener('mouseenter', () => highlight(i));
});
