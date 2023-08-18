/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    './templates/**/*.{html, js}',
    './flask_app/**/*.{html,js}',
    './flask_app/static/**/*.{html,js}',
    './src/**/*.js',
    './index.html',
    './dashboard.html'
  ],
  theme: {
    extend: {}
    },
  plugins: [{
    tailwindcss: {},
    postcss: {},
    autoprefixer: {}
  }
  ],
}

