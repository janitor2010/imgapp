<template>
  <section class="imgapp">
    <div class="imgapp__annotation">
      <div class="layout">
        <span>Задача: </span> Обучить распознавать на фотографии нужный объект. В качестве объекта был выбран утюг. Для обучения было отобрано и размечено 150 изображений.
      </div>
    </div>
    <div class="imgapp__description">
      <div class="layout">Использовалась готовая модель tensorflow object_detection. Проводилось дообучение модели. Размеченные изображения были разбиты на обучающую и тестовую выборку. Были сгенерированы TF Records. Исходная модель была дообучена для распознавания нового объекта.
      </div>
    </div>
    <div class="layout">
      <div class="imgapp__title">
          Результат:
      </div>
        <!-- <div class="imgapp__disclaimer">
          Было протестировано на реальных фотографиях и фотографиях из интернета.
        </div> -->
        <div class="imgapp__imgwrapper">
          <img v-for="i in images" :src="'static/images/'+i" alt="">
        </div>

    </div>
    <div class="imgapp__bottom">
      <a target="_blank" href="https://github.com/janitor2010"><svg-icon type="github-logo"></svg-icon></a>
    </div>
  </section>
</template>

<script>
import svgIcon from '@/components/elements/svg-icon.vue'

export default {
  name: 'app',
  data () {
    return {
        images: [
          '1.png',
          '4.png'
        ]
    }
  },
  methods: {

  },
  computed: {

  },
  components: { svgIcon }
}
</script>
<style lang="scss" scoped>



</style>
