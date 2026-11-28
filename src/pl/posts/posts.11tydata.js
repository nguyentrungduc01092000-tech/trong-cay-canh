// Permalink tinh tu slug — phong truong hop Sveltia ghi permalink rong/sai
// (/pl//) hoac khong ghi permalink. Ghi de permalink trong front matter
// (eleventyComputed co do uu tien cao hon) nhung cho ra dung URL nhu cu,
// vi moi bai deu co slug, va permalink cu cung la /pl/{{ slug }}/.
module.exports = {
  eleventyComputed: {
    permalink: (data) => `/pl/${data.slug || data.page.fileSlug}/`,
  },
};
