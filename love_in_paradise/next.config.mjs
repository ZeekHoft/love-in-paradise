// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Set the output mode to 'export' for static HTML generation
  output: 'export',

  // Optional: Disable the trailing slash for cleaner URLs
  trailingSlash: true,

  // Optional: Set a base path if the site is hosted on a sub-path (e.g., GitHub Pages)
  // basePath: '/my-static-app', 
};

export default nextConfig; // <-- Use 'export default'
