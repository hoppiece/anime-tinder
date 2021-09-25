import colors from 'vuetify/es5/util/colors'

export default {
  // Environment variable
  publicRuntimeConfig: {
    appURL: process.env.VUE_APP_APP_URL || 'http://127.0.0.1:3000',
    serverURL: process.env.VUE_APP_SERVER_URL || 'http://127.0.0.1:5000',
  },

  privateRuntimeConfig: {
  },

  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,
  vue: {
    devtools: true
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    //title: process.env.npm_package_name || '',
    titleTemplate:  '%sToonder | オタクとアニメのマッチングサービス',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@/assets/scss/app.scss'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '@/plugins/localStorage', ssr: false },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
  ],

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['@/assets/scss/vuetify_variables.scss'],
    treeShake: true,
    theme: {
      dark: false,
      themes: {
        light: {
          // ハイフン使えない
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        }
      }
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    extend(config, ctx) {
      config.node = {
        fs: "empty" // SPAでTwitterAPIを使うのに必要
      };
    }
  },
}