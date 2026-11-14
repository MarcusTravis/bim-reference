/* Shared catalog: filter chips, search, sort, and comparison-chart rows. */
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
  function row(d) {
    var tags = (d.tags || []).map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("");
    var icon = d.icon
      ? '<img class="app-icon" src="icons/' + esc(d.icon) + '.png" width="52" height="52" alt="">'
      : "";
    var site = d.url
      ? '<a class="official" href="' + esc(d.url) + '" rel="noopener noreferrer">Official site →</a>'
      : "";
    return (
      "<tr" + (d.id ? ' id="' + esc(d.id) + '"' : "") + ">" +
        '<td class="prod-cell"><div class="prod">' + icon +
          "<div><span class=\"cart\">" + esc(d.name) + '</span><span class="year">' + esc(d.maker) + "</span></div></div></td>" +
        '<td class="purpose">' + esc(d.knownFor) + '<div class="tags">' + tags + "</div></td>" +
        extraCells(d) +
        "<td>" + stars(d.pop) + '<span class="sub">' + esc(d.popCaption) + "</span></td>" +
        "<td>" + dollars(d.cost) + '<span class="sub">' + esc(d.costCaption) + "</span></td>" +
        "<td>" + (d.learn ? esc(d.learn) : "") + "</td>" +
        '<td class="purpose"><div class="pc"><span class="pro">+ ' + esc(d.pro) + '</span><span class="con">− ' + esc(d.con) + "</span></div></td>" +
        "<td>" + site + "</td>" +
      "</tr>"
    );
  }
  function extraCells(d) {
    return extraCols.map(function (k) {
      return '<td class="hw">' + esc(d[k]) + "</td>";
    }).join("");
  }
  var extraCols = [];
  function norm(s) { return String(s || "").toLowerCase(); }

  function dirFor(sortKey) {
    if (sortKey === "name" || sortKey === "cost-asc" || sortKey === "pop-asc") return "asc";
    if (sortKey === "name-desc" || sortKey === "pop" || sortKey === "cost-desc") return "desc";
    return null;
  }
  function headerKey(sortKey) {
    if (sortKey === "cost-asc" || sortKey === "cost-desc") return "cost";
    if (sortKey === "name-desc") return "name";
    if (sortKey === "pop-asc") return "pop";
    return sortKey;
  }

  window.initCatalog = function (DATA, opts) {
    opts = opts || {};
    var noun = opts.noun || "products";
    extraCols = opts.extraCols || [];
    var filter = "all", query = "", sortKey = opts.defaultSort || "pop";
    var rowsEl = document.getElementById("rows");
    var countEl = document.getElementById("count");
    if (!rowsEl) return;

    function matches(d) {
      if (filter !== "all" && !(d.tags || []).includes(filter)) return false;
      if (!query) return true;
      var extras = extraCols.map(function (k) { return d[k]; }).join(" ");
      var blob = [d.name, d.maker, d.knownFor, (d.tags || []).join(" "), d.pro, d.con, extras].join(" ");
      return norm(blob).indexOf(query) !== -1;
    }
    function sorted(rows) {
      rows = rows.slice();
      if (sortKey === "name") rows.sort(function (a, b) { return a.name.localeCompare(b.name); });
      else if (sortKey === "name-desc") rows.sort(function (a, b) { return b.name.localeCompare(a.name); });
      else if (sortKey === "pop") rows.sort(function (a, b) { return (b.pop || 0) - (a.pop || 0) || a.name.localeCompare(b.name); });
      else if (sortKey === "pop-asc") rows.sort(function (a, b) { return (a.pop || 0) - (b.pop || 0) || a.name.localeCompare(b.name); });
      else if (sortKey === "cost-asc") rows.sort(function (a, b) { return (a.cost || 0) - (b.cost || 0) || a.name.localeCompare(b.name); });
      else if (sortKey === "cost-desc") rows.sort(function (a, b) { return (b.cost || 0) - (a.cost || 0) || a.name.localeCompare(b.name); });
      return rows;
    }
    function syncControls() {
      var sort = document.getElementById("sort");
      if (sort) {
        var opt = sortKey;
        if (opt === "pop-asc") opt = "pop";
        if (opt === "name-desc") opt = "name";
        if ([].some.call(sort.options, function (o) { return o.value === opt; })) sort.value = opt;
      }
      document.querySelectorAll(".th-btn").forEach(function (b) {
        var k = b.getAttribute("data-k");
        if (k === headerKey(sortKey)) b.setAttribute("data-dir", dirFor(sortKey) || "desc");
        else b.removeAttribute("data-dir");
      });
    }
    function resetFilters() {
      filter = "all"; query = "";
      document.querySelectorAll(".chip").forEach(function (c) {
        c.setAttribute("aria-pressed", c.getAttribute("data-f") === "all" ? "true" : "false");
      });
      var s = document.getElementById("search");
      if (s) s.value = "";
    }
    // Deep links: section.html#p-product-id scrolls to that row and flashes it.
    var realign = function () {};
    function focusHash(smooth) {
      var id = decodeURIComponent((location.hash || "").slice(1));
      if (!id || !/^p-/.test(id)) return;
      if (!DATA.some(function (d) { return d.id === id; })) return;
      var tr = document.getElementById(id);
      if (!tr) { resetFilters(); render(); tr = document.getElementById(id); }
      if (!tr) return;
      var box = tr.closest(".table-box");
      if (box) box.scrollLeft = 0;
      function go(behavior) {
        var nav = document.querySelector(".topnav");
        var navH = nav ? nav.getBoundingClientRect().height : 0;
        var y = tr.getBoundingClientRect().top + window.pageYOffset - navH - 20;
        window.scrollTo({ top: Math.max(0, y), behavior: behavior });
      }
      realign = function () { go("instant"); };
      go(smooth ? "smooth" : "instant");
      // Re-align once fonts and icons have settled, unless the reader already scrolled away.
      var settled = window.pageYOffset;
      setTimeout(function () { if (Math.abs(window.pageYOffset - settled) < 4) go("instant"); }, 450);
      document.querySelectorAll("tr.row-flash").forEach(function (r) { r.classList.remove("row-flash"); });
      void tr.offsetWidth;
      tr.classList.add("row-flash");
      setTimeout(function () { tr.classList.remove("row-flash"); }, 3200);
    }
    function render() {
      var rows = sorted(DATA.filter(matches));
      rowsEl.innerHTML = rows.map(row).join("") ||
        '<tr><td colspan="' + (7 + extraCols.length) + '" class="empty">No products match those filters. Clear search or choose All.</td></tr>';
      if (countEl) countEl.textContent = "Showing " + rows.length + " of " + DATA.length + " " + noun;
      syncControls();
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
      sort.addEventListener("change", function () {
        sortKey = sort.value;
        render();
      });
    }
    document.querySelectorAll(".th-btn").forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-k");
        if (k === "name") sortKey = (sortKey === "name") ? "name-desc" : "name";
        else if (k === "pop") sortKey = (sortKey === "pop") ? "pop-asc" : "pop";
        else if (k === "cost") sortKey = (sortKey === "cost-asc") ? "cost-desc" : "cost-asc";
        render();
      });
    });
    render();
    if (location.hash) {
      focusHash(false);
      if (document.readyState !== "complete") {
        var y0 = window.pageYOffset;
        window.addEventListener("load", function () {
          // Icons and fonts can shift rows a little; line up again if the reader has not scrolled.
          if (Math.abs(window.pageYOffset - y0) < 4) realign();
        });
        setTimeout(function () { y0 = window.pageYOffset; }, 500);
      }
    }
    window.addEventListener("hashchange", function () { focusHash(true); });
  };
})();
