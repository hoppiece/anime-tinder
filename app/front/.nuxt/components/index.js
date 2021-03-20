export { default as AppBar } from '../../components/AppBar.vue'
export { default as CaptionBox } from '../../components/CaptionBox.vue'
export { default as LikeButton } from '../../components/LikeButton.vue'
export { default as Loading } from '../../components/Loading.vue'
export { default as LoginButton } from '../../components/LoginButton.vue'
export { default as NavSideBar } from '../../components/NavSideBar.vue'
export { default as NopeButton } from '../../components/NopeButton.vue'
export { default as ResultButton } from '../../components/ResultButton.vue'
export { default as SNSShareButton } from '../../components/SNSShareButton.vue'
export { default as SuperLikeButton } from '../../components/SuperLikeButton.vue'
export { default as TheResultAnimeInfo } from '../../components/TheResultAnimeInfo.vue'
export { default as TheResultTextBox } from '../../components/TheResultTextBox.vue'
export { default as TitleImages } from '../../components/TitleImages.vue'

export const LazyAppBar = import('../../components/AppBar.vue' /* webpackChunkName: "components/app-bar" */).then(c => c.default || c)
export const LazyCaptionBox = import('../../components/CaptionBox.vue' /* webpackChunkName: "components/caption-box" */).then(c => c.default || c)
export const LazyLikeButton = import('../../components/LikeButton.vue' /* webpackChunkName: "components/like-button" */).then(c => c.default || c)
export const LazyLoading = import('../../components/Loading.vue' /* webpackChunkName: "components/loading" */).then(c => c.default || c)
export const LazyLoginButton = import('../../components/LoginButton.vue' /* webpackChunkName: "components/login-button" */).then(c => c.default || c)
export const LazyNavSideBar = import('../../components/NavSideBar.vue' /* webpackChunkName: "components/nav-side-bar" */).then(c => c.default || c)
export const LazyNopeButton = import('../../components/NopeButton.vue' /* webpackChunkName: "components/nope-button" */).then(c => c.default || c)
export const LazyResultButton = import('../../components/ResultButton.vue' /* webpackChunkName: "components/result-button" */).then(c => c.default || c)
export const LazySNSShareButton = import('../../components/SNSShareButton.vue' /* webpackChunkName: "components/s-n-s-share-button" */).then(c => c.default || c)
export const LazySuperLikeButton = import('../../components/SuperLikeButton.vue' /* webpackChunkName: "components/super-like-button" */).then(c => c.default || c)
export const LazyTheResultAnimeInfo = import('../../components/TheResultAnimeInfo.vue' /* webpackChunkName: "components/the-result-anime-info" */).then(c => c.default || c)
export const LazyTheResultTextBox = import('../../components/TheResultTextBox.vue' /* webpackChunkName: "components/the-result-text-box" */).then(c => c.default || c)
export const LazyTitleImages = import('../../components/TitleImages.vue' /* webpackChunkName: "components/title-images" */).then(c => c.default || c)
