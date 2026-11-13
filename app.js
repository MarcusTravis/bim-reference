/* Shared catalog: filter chips, search, sort, and product cards. */
(function () {
  function stars(n) {
    var full = Math.floor(n), half = (n - full) >= 0.5, empty = 5 - full - (half ? 1 : 0);
    var on = "★".repeat(full) + (half ? "½" : "");
    var off = "★".repeat(empty);
    return '<span class="starline" aria-label="' + n + ' out of 5"><span class="stars">' + on + '</span><span class="stars off">' + off + "</span></span>";
  }
  function dollars(n) {
    n = Math.max(0, Math.min(4, Number(n) || 0));
    if (n === 0) return '<span class="costline" aria-label="Free">Free</span>';
    var on = "$".repeat(n), off = "$".repeat(4 - n);
    return '<span class="costline" aria-label="' + n + ' of 4"><span class="cost-on">' + on + '</span><span class="cost-off">' + off + "</span></span>";
  }
  function esc(s) {
    return String(s ?? "").replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function card(d) {
    var tags = (d.tags || []).map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("");
    var learn = d.learn ? '<div class="learn"><b>Learning curve:</b> ' + esc(d.learn) + " <span>(editorial)</span></div>" : "";
    var costRow = '<div class="cost-row"><div class="cost-head"><b>Cost:</b> ' + dollars(d.cost) + "</div>" +
          '<span class="sub">' + esc(d.costCaption || "") + "</span></div>";
    return (
      '<article class="pcard">' +
        '<header><span class="nm">' + esc(d.name) + '</span><span class="maker">' + esc(d.maker) + "</span></header>" +
        '<p class="known">' + esc(d.knownFor) + "</p>" +
        '<div class="tags">' + tags + "</div>" +
        '<div class="pop-row"><span class="rate-lbl">Popularity</span>' + stars(d.pop) +
          '<span class="sub">' + esc(d.popCaption) + "</span></div>" +
        costRow +
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
    var cardsEl = document.getElementById("cards");
    var countEl = document.getElementById("count");
    if (!cardsEl) return;

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
      else if (sortKey === "cost-asc") rows.sort(function (a, b) { return (a.cost || 0) - (b.cost || 0) || a.name.localeCompare(b.name); });
      else if (sortKey === "cost-desc") rows.sort(function (a, b) { return (b.cost || 0) - (a.cost || 0) || a.name.localeCompare(b.name); });
      return rows;
    }
    function render() {
      var rows = sorted(DATA.filter(matches));
      cardsEl.innerHTML = rows.map(card).join("") ||
        '<p class="count">No products match those filters. Clear search or choose All.</p>';
      if (countEl) countEl.textContent = "Showing " + rows.length + " of " + DATA.length + " " + noun;
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
