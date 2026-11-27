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
  // --- Static passthrough ---
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "src/admin": "admin" });
  // Anh goc trong src/media duoc giu nguyen tai /media/ (CMS upload vao day).
  eleventyConfig.addPassthroughCopy({ "src/media": "media" });

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
    const srcPath = path.join(__dirname, src);
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
