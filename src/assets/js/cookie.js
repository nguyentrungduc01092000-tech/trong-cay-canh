// Cookie banner theo chuan EU + GoatCounter (thong ke mien phi, khong cookie).
// GoatCounter CHI tai sau khi nguoi doc bam dong y. Lua chon luu vao localStorage.
// Domain GoatCounter lay tu <html data-goatcounter="..."> — xem README muc 5.
// Neu domain van la [GIỮ CHỖ] hoac rong thi khong tai gi ca.
(function () {
  var KEY = "cookie-consent";
  var banner = document.getElementById("cookie-banner");
  var acceptBtn = document.getElementById("cookie-accept");
  var declineBtn = document.getElementById("cookie-decline");
  var domain = document.documentElement.getAttribute("data-goatcounter") || "";
  function loadGoatCounter() {
    if (!domain || domain.indexOf("GIỮ CHỖ") !== -1) return;
    if (document.querySelector('script[data-goatcounter]')) return;
    var s = document.createElement("script");
    s.async = true;
    s.setAttribute("data-goatcounter", "https://" + domain + "/count");
    s.src = "//gc.zgo.at/count.js";
    document.head.appendChild(s);
  }
  function setChoice(value) {
    try { localStorage.setItem(KEY, value); } catch (e) { /* localStorage bi chan */ }
    if (banner) banner.hidden = true;
    if (value === "accepted") loadGoatCounter();
  }
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) { /* bo qua */ }
  if (stored === "accepted") {
    loadGoatCounter();
  } else if (stored === "declined") {
    if (banner) banner.hidden = true;
  } else if (banner) {
    banner.hidden = false;
  }
  if (acceptBtn) acceptBtn.addEventListener("click", function () { setChoice("accepted"); });
  if (declineBtn) declineBtn.addEventListener("click", function () { setChoice("declined"); });
  // Link rut lai dong y o chan trang: xoa lua chon cu, hien lai banner.
  var settingsLink = document.getElementById("cookie-settings");
  if (settingsLink) settingsLink.addEventListener("click", function (e) {
    e.preventDefault();
    try { localStorage.removeItem(KEY); } catch (err) { /* bỏ qua */ }
    if (banner) banner.hidden = false;
  });
})();
