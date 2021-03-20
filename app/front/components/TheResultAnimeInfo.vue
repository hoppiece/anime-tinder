<template>
  <div>
      <v-container>
          <v-row>
              <v-col cols=12 md=3>
                  <v-img
                    src="https://www.lisani.jp/admin/wp-content/uploads/2021/01/2101101800-yh-001.jpg"
                    aspect-ratio=0.75
                    max-height=400
                    max-width=300
                    >
                  </v-img>
              </v-col>
              <v-col cols=12 md=9>
                  <v-expansion-panels flat class="mb-3">
                    <v-expansion-panel>
                        <v-expansion-panel-header><strong>概要</strong></v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <p>
                                貧乏な生活を送る高校２年生・上杉風太郎のもとに、好条件の家庭教師アルバイトの話が舞い込む。ところが教え子はなんと同級生！！　しかも五つ子だった！！全員美少女、だけど「落第寸前」「勉強嫌い」の問題児！最初の課題は姉妹からの信頼を勝ち取ること…！？毎日がお祭り騒ぎ！ 中野家の五つ子が贈る、かわいさ500％の五人五色ラブコメ開演！！
                            </p>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                  <br/>
                  <v-expansion-panels flat class="mb-3">
                    <v-expansion-panel>
                        <v-expansion-panel-header><strong>キャスト/スタッフ</strong></v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <p>[キャスト]上杉風太郎:松岡禎丞／中野一花:花澤香菜／中野ニ乃:竹達彩奈／中野三玖:伊藤美来／中野四葉:佐倉綾音／中野五月:水瀬いのり</p>
                            <p>[スタッフ]原作:春場ねぎ（講談社「週刊少年マガジン」）／監督:かおり／シリーズ構成:大知慶一郎／キャラクターデザイン・総作画監督:勝又聖人／美術監督:扇山秋仁／色彩設計:松山愛子／撮影監督:千葉大輔／編集:武宮むつみ／音響監督:髙桑 一／音楽:中村巴奈重・櫻井美希／音楽制作:日音／音響制作:ダックスプロダクション／アニメーション制作:バイブリーアニメーションスタジオ</p>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                  <!--ハッシュタグ・動画リンク-->
                  <div>
                    <v-row>
                        <v-col cols=12 md=8>
                            <h4>#2021年春 #ハーレム #ラブコメ #学園</h4>
                            <v-btn href="https://anime.dmkt-sp.jp/animestore/sch_pc?searchKey=%E4%BA%94%E7%AD%89%E5%88%86%E3%81%AE%E8%8A%B1%E5%AB%81%E2%88%AC&vodTypeList=svod_tvod" target="_blank" rel="noopener noreferrer" style="text-transform: none" color="#EB5528" dark x-small>
                                <strong>dアニメストア</strong></v-btn>
                            <v-btn href="https://www.amazon.co.jp/s?k=%E4%BA%94%E7%AD%89%E5%88%86%E3%81%AE%E8%8A%B1%E5%AB%81%E2%88%AC&i=instant-video" target="_blank" rel="noopener noreferrer" style="text-transform: none" color="#01A7E1" dark x-small>
                                Amazon Prime Video
                            </v-btn>
                        </v-col>
                        <v-col cols=12 md=4>
                            <v-btn @click="restart" block color="white" class="mt-2"><strong>もう1回診断する</strong></v-btn>
                        </v-col>
                    </v-row>
                  </div>

              </v-col>
          </v-row>
      </v-container>
  </div>
</template>
<script>
export default {
  methods: {
     restart: function () {
        this.$router.push('/');
    },
  }
};
</script>
