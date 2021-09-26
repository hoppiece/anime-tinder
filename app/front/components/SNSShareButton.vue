<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols=3>
          <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
              <v-btn @click="share('twitter')" color="#1C9BE9" dark block v-bind="attrs" v-on="on"><v-icon>mdi-twitter</v-icon></v-btn>
            </template>
          <span>Twitterで共有する</span>
          </v-tooltip>
        </v-col>

        <v-col cols=3>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn @click="share('line')" color="#06C755" dark block v-bind="attrs" v-on="on"><strong>LINE</strong></v-btn>
            </template>
            <span>LINEで共有する</span>
          </v-tooltip>
        </v-col>

        <v-col cols=3>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn @click="share('facebook')" color="#4064AC" dark block v-bind="attrs" v-on="on"><v-icon>mdi-facebook</v-icon></v-btn>
            </template>
            <span>Facebookで共有する</span>
          </v-tooltip>
        </v-col>

          <v-col cols=3>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn @click="share('hatena')" color="#00A4DE" dark block v-bind="attrs" v-on="on"><strong>B!</strong></v-btn>
              </template>
              <span>はてなブックマークで共有する</span>
            </v-tooltip>
          </v-col>

        </v-row>
      </v-container>

    <v-container fluid>
      <v-textarea
        name="input-7-1"
        filled
        label="コピペ用"
        auto-grow
        :rules="rules"
        :value="value1+title+value2"
        counter
        background-color="white"
        clearable
      ></v-textarea>
    </v-container>
  </div>
</template>


<script>
  export default {
    props: {
      title: String,
    },
    data: () => ({
      rules: [v => !!v || '',
              v => (!!v && v.length <= 140) || `Max 140 characters`],
      text1: "あなたにオススメのアニメは",
      text2: "です！\n\n----オタクとアニメのマッチングサービスToonder",
      hashtag: "Toonder,技育CAMP,ハッカソン",
      value1: "あなたにオススメのアニメは",
      value2: "です！\n\n----オタクとアニメのマッチングサービスToonder \n#Toonder #技育CAMP #ハッカソン",
    }),

    methods: {
      share(sns) {
        const shareUrl = this.$config.appURL + this.$route.path
        console.log(shareUrl)
        let href = ""
        switch( sns ) {
          case 'twitter':
              href = `https://twitter.com/intent/tweet?hashtags=`+this.hashtag+`&text=`+this.text1+this.title+this.text2+`&url=`+shareUrl
              // href = `https://twitter.com/intent/tweet?hashtags=`+this.hashtag+`&text=`+this.text1+this.title+this.text2
              break
          case 'facebook':
              href = `https://www.facebook.com/sharer/sharer.php`
              break
          case 'line':
              href = `https://line.me/R/msg/text/?`+this.text1+this.title+this.text2
              break
          case 'hatena':
              // href = `http://b.hatena.ne.jp/add?&url=`+shareUrl
              href = `http://b.hatena.ne.jp/add`
              break
        }
        if(sns=="line"){
          window.open(href, '_blank')
        }else{
          window.open(href, '_blank',"rel=nofollow noopener noreferrer")
        }
      },
    },
  }
</script>


