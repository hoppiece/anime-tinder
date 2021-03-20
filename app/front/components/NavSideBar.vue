<template>
  <!-- 色付きドロワー -->
  <v-navigation-drawer
    app
    v-model="drawer"
    clipped
    class="accent-4"
    permanent
  >
    <v-list-item dark class="horizontal-gradient" id="nav-user" v-on:click="open">
      <v-list-item-content>
        <v-list-item-title>
          <img :src="userImage" class="nav-icon-line">
          <h3 class="nav-icon-line">&nbsp;@{{$store.state.userName}}</h3>
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item dark class="horizontal-gradient" id="nav-logout" :class="{ isOpen }" v-on:click="logout">
      <v-list-item-content>
        <v-list-item-title>
          <h3 class="nav-icon-line">Logout</h3>
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider></v-divider>

    <!-- 履歴表示 -->
    <h3 id="recent-title">最近の診断結果</h3>
    <v-row justify="center">
      <v-col
        v-for="item in items"
        :key="item.title"
        :href="item.to"
        cols=5
        class="d-flex child-flex"
      >
        <v-img :src="item.imageUrl" ></v-img>
      </v-col>
    </v-row>
    <!--v-list>
      <v-list-item
        v-for="item in items"
        :key="item.title"
        :href="item.to"
      >
        <v-list-item-content>
          <v-card
            dark
            class="mx-auto"
            :img="item.imageUrl"
            height="250"
          >
          </v-card>
        </v-list-item-content>
      </v-list-item>
    </v-list-->
  </v-navigation-drawer>
</template>

<script>
import axios from 'axios';
export default {
  data () {
    return {
      drawer: true,
      isOpen: false,
      userImage: this.$store.state.userImage,
      items: [
        { title: '五等分の花嫁', imageUrl: "https://animeanime.jp/imgs/p/jtKDOVlKAvjRrNw8SXAVejagI61Nrq_oqaqr/359929.jpg", to: "/result/gotoubun" },
        { title: '呪術廻戦', imageUrl: "https://pbs.twimg.com/media/Epkl6M8VoAAGZAP.jpg", to: "/result/jyujyutsu" },
        { title: 'リゼロ', imageUrl: "https://eiga.k-img.com/images/anime/news/112498/photo/a8c42bc0e5f54dc2/320.jpg?1607668254", to: "/result/rezero" },
        { title: 'はたらく細胞', imageUrl: "https://assets.numan.tokyo/media/articles/images/000/008/367/large/b5b3dba5-f3a8-41af-b775-0bf08c1b7346.jpg?1584837573", to: "/result/hataraku" },
        { title: 'ゆるキャン△', imageUrl: "https://dengekionline.com/images/U6Eo/iVNf/gAfD/JWlv/Vkjtk62p9OOmOlk5ovvHfnSD7BsrhFp0IYEPVWKXQjNE4bjLhjQ2ETa8nvAKQkPdow0ld9prCOr91ahW.jpg", to: "/result/yurukyan" },
        { title: 'PUIPUIモルカー', imageUrl: "https://media.image.infoseek.co.jp/isnews/photos/eigacom/eigacom_20201222001_0.jpg", to: "result/molcar"}
      ],
    }
  },
  methods: {
    open: function () {
      this.isOpen = !this.isOpen;
    },
    logout: function () {
      // var auth = this.$store.state.authUser;
      // // logoutされてからリダイレクト
      // await axios.get(this.$config.serverURL + '/user/logout', {
      //   params: auth,
      // }).then(res => {
      //   // logout
      //   this.$store.commit('setAuthUser', null);
      //   this.$store.commit('setUserName', null);
      //   this.$store.commit('setUserImage', null);
      //   this.$router.push('/login');
      // }).catch(err => {
      //   // error
      // });

      // サーバからのリダイレクトがうまくいかない。一旦簡易的にログアウト
      this.$store.commit('setAuthUser', null);
      this.$store.commit('setUserName', null);
      this.$store.commit('setUserImage', null);
      this.$router.push('/login');
    },
  },
}
</script>