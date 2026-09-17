(function () {
  var el = document.currentScript;
  var id = el && el.getAttribute("data-ga4-id");
  if (!id || !window) return;
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", id);
})();
