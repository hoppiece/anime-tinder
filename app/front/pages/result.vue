<template>
    <div class="home-background mt-5">
        <TheResultTextBox/>
        <TheResultAnimeInfo/>
        <CaptionBox title="結果をシェアする" />
        <SNSShareButton/>
        <CaptionBox title="みんなの診断結果" />
    </div>
</template>

<script>
import TheResultTextBox from '~/components/TheResultTextBox.vue'
import TheResultAnimeInfo from '~/components/TheResultAnimeInfo.vue'
import CaptionBox from '~/components/CaptionBox.vue'
import SNSShareButton from '~/components/SNSShareButton.vue'

export default {
  // middleware: 'authenticated',
  components: {
      TheResultTextBox,
      TheResultAnimeInfo,
      CaptionBox,
      SNSShareButton,
  },
  data() {
    return {
      name: 'result',
    }
  },
}
</script>