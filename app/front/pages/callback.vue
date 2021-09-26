<template>
  <Loading v-show="loading"></Loading>
</template>

<script>
import axios from 'axios';
import Loading from '@/components/Loading';

export default {
  components: {
    Loading,
  },
  data() {
    return {
      loading: true,
      name: 'callback',
    }
  },
  head() {
    return {
      title: '',
    }
  },
  async mounted() {
    await axios.get(this.$config.serverURL+'/user/callback', {
      params: this.$route.query,
    }).then(res => {
      // set session
      this.$store.commit('setAuthUser', res.data.sessionId);
      this.$store.commit('setUserName', res.data.username);
      this.$store.commit('setUserImage', res.data.profile_image_url);
      this.loading = false;
      this.$router.push('/');
    }).catch(err => {
      console.log(err)
    });
  },
};
</script>
