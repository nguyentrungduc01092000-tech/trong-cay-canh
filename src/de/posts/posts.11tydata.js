// Permalink tinh tu slug — phong truong hop Sveltia ghi permalink rong/sai
// (/de//) hoac khong ghi permalink. Ghi de permalink trong front matter
// (eleventyComputed co do uu tien cao hon) nhung cho ra dung URL nhu cu,
// vi moi bai deu co slug, va permalink cu cung la /de/{{ slug }}/.
module.exports = {
  eleventyComputed: {
    permalink: (data) => `/de/${data.slug || data.page.fileSlug}/`,
  },
};
