(function () {
  document.documentElement.classList.add("has-js");
  const nodes = document.querySelectorAll("[data-include]");
  if (!nodes.length) {
    document.dispatchEvent(new CustomEvent("partials:ready"));
    return;
  }

  Promise.all(
    Array.from(nodes).map(function (node) {
      var src = node.getAttribute("data-include");
      return fetch(src, { cache: "no-store" })
        .then(function (res) {
          if (!res.ok) throw new Error(src);
          return res.text();
        })
        .then(function (html) {
          node.outerHTML = html;
        })
        .catch(function () {
          /* file:// або мере partial — лишаємо inline-fallback всередині node */
          node.removeAttribute("data-include");
        });
    })
  ).finally(function () {
    document.dispatchEvent(new CustomEvent("partials:ready"));
  });
})();
