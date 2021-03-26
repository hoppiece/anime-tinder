<template>
  <div>
    <v-app-bar
      class="horizontal-gradient"
      dark
      dense
      flat
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" @click="getRecent" ></v-app-bar-nav-icon>
      <v-toolbar-title @click="goHome">Toonder</v-toolbar-title>
    </v-app-bar>

    <!--左の三ボタン押したら開くやつ-->
    <v-navigation-drawer
    app
    v-model="drawer"
    clipped
    class="accent-4"
    >
    <!--Twitterアイコン関連-->
    <v-list-item dark class="horizontal-gradient-reverse" id="nav-user" v-on:click="open">
      <v-list-item-content>
        <v-list-item-title>
          <img :src="userImage" class="nav-icon-line">
          <h3 class="nav-icon-line">&nbsp;@{{$store.state.userName}}</h3>
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item dark class="horizontal-gradient-reverse" id="nav-logout" :class="{ isOpen }" v-on:click="logout">
      <v-list-item-content>
        <v-list-item-title>
          <h3 class="nav-icon-line">Logout</h3>
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider></v-divider>

    <!--最近の診断結果-->
    <h3 id="recent-title">最近の診断結果</h3>
        <v-row justify="center">
            <v-col
                v-for="item in items"
                :key="item.id"
                cols=5
                class="d-flex child-flex">
                <v-img :src="'data:image/jpg;base64,'+item.image"  @click="openResult(item.id)"></v-img>
            </v-col>
        </v-row>
    </v-navigation-drawer>

  </div>
</template>


<script>
import axios from 'axios';
export default {
  data() {
    return {
      drawer: false,
      group: null,
      isOpen: false,
      userImage: this.$store.state.userImage,
      items: [],
    }
  },
  // 最近の診断結果を10件まで取得
  async mounted() {
    this.getRecent();
  },
  watch: {
    group () {
      this.drawer = false
    },
  },
  methods: {
    open: async function () {
    this.isOpen = !this.isOpen;
    },
    getRecent: async function() {
      await axios.post(this.$config.serverURL+'/user/recent', {
        num : 10,
        sessionID: this.$store.state.authUser,
      }).then(res => {
        this.items = res.data.animes;
      }).catch(err => {
      });
    },
    logout: function () {
    // サーバからのリダイレクトがうまくいかない。簡易的にログアウト
    this.$store.commit('setAuthUser', null);
    this.$store.commit('setUserName', null);
    this.$store.commit('setUserImage', null);
    this.$store.commit('setStarted', true);
    this.$router.push('/login');
    },
    // 画像をクリックすると結果ページに遷移
    openResult: function (animeId) {
      this.$router.push({  path: `/result/${animeId}`  });
    },
    goHome: function () {
      this.$router.push('/');
    }
  },
}
</script>