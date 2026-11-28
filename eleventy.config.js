// Eleventy config — demo web truyen hu cau DE/PL (GitHub Pages, tinh).
const Image = require("@11ty/eleventy-img").default; // eleventy-img v7 la ESM: can .default khi require tu CommonJS
const path = require("path");

function isPublished(post) {
  if (!post.data) return false;
  if (post.data.draft === true) return false;
  const d = post.date ? new Date(post.date) : null;
  if (d && d > new Date()) return false; // bai hen gio: chi len khi rebuild sau ngay dang
  return true;
}
function isScheduled(post) {
  if (!post.data || post.data.draft === true) return false;
  const d = post.date ? new Date(post.date) : null;
  return d && d > new Date();
}

module.exports = function (eleventyConfig) {
  // --- Loc ngon ngu luc build (Phuong an A, Ruler 15:52 27/11) ---
  // SITE_LANG=de -> chi dung tieng Duc (sunbow.click); SITE_LANG=pl -> chi
  // dung tieng Ba Lan (plasma.click); khong dat -> dung ca 2 ngon ngu (ban
  // gop cu, chi dung khi phat trien local). File .md ngon ngu kia GIU NGUYEN
  // trong repo (khong xoa) — chi loai khoi ban build.
  const SITE_LANG = process.env.SITE_LANG || "";
  if (SITE_LANG && SITE_LANG !== "de" && SITE_LANG !== "pl") {
    throw new Error(`SITE_LANG khong hop le: ${JSON.stringify(SITE_LANG)} (chi duoc "de" hoac "pl")`);
  }
  const OTHER_LANG = SITE_LANG === "de" ? "pl" : SITE_LANG === "pl" ? "de" : "";
  if (OTHER_LANG) {
    // Loai toan bo cay ngon ngu kia khoi build (bai, trang index, chuyen muc,
    // trang phap ly, search.json) — _site se khong co file nao cua ngon ngu do.
    eleventyConfig.ignores.add(`src/${OTHER_LANG}/**`);
  }
  if (SITE_LANG === "pl") {
    // Dashboard la trang tieng Duc (canonical sunbow) — chi co tren ban de.
    eleventyConfig.ignores.add("src/dashboard.njk");
  }
  // Cho template biet dang build ngon ngu nao ("de" | "pl" | "both").
  eleventyConfig.addGlobalData("build_lang", SITE_LANG || "both");

  // --- Static passthrough ---
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "src/admin": "admin" });
  // Anh goc trong src/media duoc giu nguyen tai /media/ (CMS upload vao day).
  eleventyConfig.addPassthroughCopy({ "src/media": "media" });
  eleventyConfig.addPassthroughCopy("src/ads.txt");

  // --- Bo loc ngay ban dia: {{ date | dateLocalized('de-DE') }} ---
  eleventyConfig.addFilter("dateLocalized", (date, locale) => {
    if (!date) return "";
    return new Intl.DateTimeFormat(locale || "de-DE", {
      day: "numeric",
      month: "long",
      year: "numeric",
    }).format(new Date(date));
  });
  eleventyConfig.addFilter("wordCount", (text) => {
    if (!text) return 0;
    return String(text).replace(/<[^>]+>/g, " ").trim().split(/\s+/).length;
  });
  // Bo loc date toi gian kieu strftime: %Y, %m, %d (dung cho datetime + nam ban quyen).
  eleventyConfig.addFilter("date", (value, format) => {
    const d = value === "now" ? new Date() : new Date(value);
    if (isNaN(d)) return "";
    const pad = (n) => String(n).padStart(2, "0");
    return (format || "%Y-%m-%d")
      .replace("%Y", d.getFullYear())
      .replace("%m", pad(d.getMonth() + 1))
      .replace("%d", pad(d.getDate()));
  });

  // --- Shortcode anh responsive: nhieu co + dinh dang hien dai, giu anh goc ---
  // Dung: {% image "src/media/covers/hund.jpg", "Mo ta anh", "eager" %}
  eleventyConfig.addAsyncShortcode("image", async function (src, alt, loading) {
    // Sveltia ghi cover dang /media/... (theo public_folder); file doi viet
    // dang src/media/... — chap nhan ca 2, deu tro toi src/media/... tren dia.
    // (Khong doi public_folder trong config: doi se lam hong xem truoc anh
    // trong admin Sveltia.)
    let diskSrc = src;
    if (diskSrc.startsWith("/media/")) diskSrc = "src" + diskSrc;
    const srcPath = path.join(__dirname, diskSrc);
    const metadata = await Image(srcPath, {
      widths: [400, 800, 1200],
      formats: ["avif", "webp", "jpeg"],
      outputDir: "./_site/img/",
      urlPath: "/img/",
      filenameFormat: function (id, src, width, format) {
        const name = path.basename(src, path.extname(src));
        return `${name}-${width}w.${format}`;
      },
    });
    return Image.generateHTML(metadata, {
      alt: alt || "",
      loading: loading || "lazy",
      decoding: "async",
      sizes: "(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px",
    });
  });

  // --- Bo loc chuyen muc: URL trang chuyen muc + loc bai theo ten chuyen muc ---
  // categories.json la nguon chuan cho ten hien thi (de/pl) + key (slug).
  const categories = require("./src/_data/categories.json");
  eleventyConfig.addFilter("categoryUrl", (name, lang) => {
    if (!name) return "";
    const found = categories.find((c) => c[lang] === name);
    if (!found) return "";
    return `/${lang}/${lang === "de" ? "kategorie" : "kategoria"}/${found.key}/`;
  });
  eleventyConfig.addFilter("postsInCategory", (posts, name) => {
    if (!posts || !name) return [];
    return posts.filter((p) => p.data && p.data.category === name);
  });
  eleventyConfig.addFilter("categoryCount", (posts, name) => {
    if (!posts || !name) return 0;
    return posts.filter((p) => p.data && p.data.category === name).length;
  });

  // --- Collections: bai da dang (khong nhap, khong hen gio) ---
  function postsFor(lang) {
    return (collectionApi) => {
      const glob = `src/${lang}/posts/*.md`;
      return collectionApi
        .getFilteredByGlob(glob)
        .filter(isPublished)
        .sort((a, b) => b.date - a.date);
    };
  }
  function allFor(lang) {
    return (collectionApi) => {
      const glob = `src/${lang}/posts/*.md`;
      return collectionApi
        .getFilteredByGlob(glob)
        .filter((p) => p.data && p.data.draft !== true)
        .sort((a, b) => b.date - a.date);
    };
  }
  function scheduledFor(lang) {
    return (collectionApi) =>
      collectionApi.getFilteredByGlob(`src/${lang}/posts/*.md`).filter(isScheduled);
  }
  eleventyConfig.addCollection("posts_de", postsFor("de"));
  eleventyConfig.addCollection("posts_pl", postsFor("pl"));
  eleventyConfig.addCollection("all_de", allFor("de"));
  eleventyConfig.addCollection("all_pl", allFor("pl"));
  eleventyConfig.addCollection("scheduled_de", scheduledFor("de"));
  eleventyConfig.addCollection("scheduled_pl", scheduledFor("pl"));

  return {
    dir: { input: "src", output: "_site", includes: "_includes", data: "_data" },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    templateFormats: ["md", "njk", "html"],
  };
};
