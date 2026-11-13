/* Shared catalog: filter chips, search, sort, and product cards. */
(function () {
  function stars(n) {
    var full = Math.floor(n), half = (n - full) >= 0.5, empty = 5 - full - (half ? 1 : 0);
    var on = "★".repeat(full) + (half ? "½" : "");
    var off = "★".repeat(empty);
    return '<span class="stars" aria-label="' + n + ' out of 5">' + on + '</span><span class="stars off">' + off + "</span>";
  }
  function esc(s) {
    return String(s ?? "").replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function card(d) {
    var tags = (d.tags || []).map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("");
    var price = d.price ? '<div class="price"><b>Price:</b> ' + esc(d.price) + "</div>" : "";
    var learn = d.learn ? '<div class="learn"><b>Learning curve:</b> ' + esc(d.learn) + " <span>(editorial)</span></div>" : "";
    return (
      '<article class="pcard">' +
        '<header><span class="nm">' + esc(d.name) + '</span><span class="maker">' + esc(d.maker) + "</span></header>" +
        '<p class="known">' + esc(d.knownFor) + "</p>" +
        '<div class="tags">' + tags + "</div>" +
        price +
        '<div class="pop-row">' + stars(d.pop) +
          '<span class="sub">' + esc(d.popCaption) + "</span></div>" +
        learn +
        '<div class="pc"><span class="pro">+ ' + esc(d.pro) + '</span><span class="con">− ' + esc(d.con) + "</span></div>" +
        (d.url ? '<a class="official" href="' + esc(d.url) + '" rel="noopener noreferrer">Official site →</a>' : "") +
      "</article>"
    );
  }
  function norm(s) { return String(s || "").toLowerCase(); }

  window.initCatalog = function (DATA, opts) {
    opts = opts || {};
    var noun = opts.noun || "products";
    var filter = "all", query = "", sortKey = opts.defaultSort || "pop";
    var root = document.getElementById("catalog");
    if (!root) return;

    function matches(d) {
      if (filter !== "all" && !(d.tags || []).includes(filter)) return false;
      if (!query) return true;
      var blob = [d.name, d.maker, d.knownFor, (d.tags || []).join(" "), d.pro, d.con].join(" ");
      return norm(blob).indexOf(query) !== -1;
    }
    function sorted(rows) {
      rows = rows.slice();
      if (sortKey === "name") rows.sort(function (a, b) { return a.name.localeCompare(b.name); });
      else if (sortKey === "pop") rows.sort(function (a, b) { return (b.pop || 0) - (a.pop || 0) || a.name.localeCompare(b.name); });
      return rows;
    }
    function render() {
      var rows = sorted(DATA.filter(matches));
      document.getElementById("cards").innerHTML = rows.map(card).join("") ||
        '<p class="count">No products match those filters. Clear search or choose All.</p>';
      document.getElementById("count").textContent = "Showing " + rows.length + " of " + DATA.length + " " + noun;
    }

    document.querySelectorAll(".chip").forEach(function (b) {
      b.addEventListener("click", function () {
        filter = b.getAttribute("data-f");
        document.querySelectorAll(".chip").forEach(function (c) {
          c.setAttribute("aria-pressed", c === b ? "true" : "false");
        });
        render();
      });
    });
    var search = document.getElementById("search");
    if (search) {
      search.addEventListener("input", function () {
        query = norm(search.value.trim());
        render();
      });
    }
    var sort = document.getElementById("sort");
    if (sort) {
      sort.value = sortKey;
      sort.addEventListener("change", function () {
        sortKey = sort.value;
        render();
      });
    }
    render();
  };
})();
