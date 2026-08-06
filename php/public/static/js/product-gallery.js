(function () {
  var root = document.querySelector("[data-product-gallery]");
  if (!root) return;
  var main = root.querySelector("#product-gallery-main");
  root.querySelectorAll(".product-gallery-thumb").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var src = btn.getAttribute("data-gallery-src");
      if (!src || !main) return;
      main.src = src;
      root.querySelectorAll(".product-gallery-thumb").forEach(function (b) {
        b.classList.toggle("is-active", b === btn);
      });
    });
  });
})();
