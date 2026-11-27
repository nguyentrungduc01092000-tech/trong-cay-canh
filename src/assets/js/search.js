// Tim kiem client-side: doc chi muc JSON sinh o buoc build (khong goi server).
(function () {
  var input = document.getElementById("search-input");
  var list = document.getElementById("post-grid");
  var empty = document.getElementById("search-empty");
  if (!input || !list) return;
  var indexUrl = input.getAttribute("data-index");
  var cards = Array.prototype.slice.call(list.querySelectorAll(".card"));
  var index = null;
  function normalize(s) {
    // NFD khong tach duoc "ł" (khong co dang phan tach chuan) va "ß" — thay tay.
    return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/ł/g, "l").replace(/ß/g, "ss");
  }
  function apply(q) {
    var needle = normalize(q.trim());
    var shown = 0;
    cards.forEach(function (card) {
      var hay = normalize(card.getAttribute("data-search") || card.textContent);
      var ok = !needle || hay.indexOf(needle) !== -1;
      card.style.display = ok ? "" : "none";
      if (ok) shown++;
    });
    if (empty) empty.hidden = shown !== 0;
  }
  input.addEventListener("input", function () { apply(input.value); });
  // Nap chi muc JSON (tieu de + mo ta + the) de tim ca bai chua hien tren trang chu.
  if (indexUrl) {
    fetch(indexUrl).then(function (r) { return r.json(); }).then(function (data) {
      index = data;
      cards.forEach(function (card) {
        var slug = card.getAttribute("data-slug");
        var item = index.find(function (e) { return e.slug === slug; });
        if (item) card.setAttribute("data-search", [item.title, item.description, (item.tags || []).join(" "), item.category].join(" "));
      });
    }).catch(function () { /* giu tim kiem theo noi dung the bai */ });
  }
})();
