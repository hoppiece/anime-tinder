import Vue from 'vue'

const components = {
  AppBar: () => import('../../components/AppBar.vue' /* webpackChunkName: "components/app-bar" */).then(c => c.default || c),
  CaptionBox: () => import('../../components/CaptionBox.vue' /* webpackChunkName: "components/caption-box" */).then(c => c.default || c),
  LikeButton: () => import('../../components/LikeButton.vue' /* webpackChunkName: "components/like-button" */).then(c => c.default || c),
  Loading: () => import('../../components/Loading.vue' /* webpackChunkName: "components/loading" */).then(c => c.default || c),
  LoginButton: () => import('../../components/LoginButton.vue' /* webpackChunkName: "components/login-button" */).then(c => c.default || c),
  NavSideBar: () => import('../../components/NavSideBar.vue' /* webpackChunkName: "components/nav-side-bar" */).then(c => c.default || c),
  NopeButton: () => import('../../components/NopeButton.vue' /* webpackChunkName: "components/nope-button" */).then(c => c.default || c),
  ResultButton: () => import('../../components/ResultButton.vue' /* webpackChunkName: "components/result-button" */).then(c => c.default || c),
  SNSShareButton: () => import('../../components/SNSShareButton.vue' /* webpackChunkName: "components/s-n-s-share-button" */).then(c => c.default || c),
  SuperLikeButton: () => import('../../components/SuperLikeButton.vue' /* webpackChunkName: "components/super-like-button" */).then(c => c.default || c),
  TheResultAnimeInfo: () => import('../../components/TheResultAnimeInfo.vue' /* webpackChunkName: "components/the-result-anime-info" */).then(c => c.default || c),
  TheResultTextBox: () => import('../../components/TheResultTextBox.vue' /* webpackChunkName: "components/the-result-text-box" */).then(c => c.default || c),
  TitleImages: () => import('../../components/TitleImages.vue' /* webpackChunkName: "components/title-images" */).then(c => c.default || c)
}

for (const name in components) {
  Vue.component(name, components[name])
  Vue.component('Lazy' + name, components[name])
}
