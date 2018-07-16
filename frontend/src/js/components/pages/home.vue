<template>
  <section class="main">
    <div class="layout">
    <h1>Белая Любовь</h1>
    <div class="main__logo"></div>
    <div class="main__title">
      Skills:
    </div>
    <div class="main__skills">
      <div :class="'main__skills-item-'+randomInt()" v-for="skill in skills" v-html="skill" class="main__skills-item"></div>
    </div>
    <div class="main__title">
      Проекты можно посмотреть по ссылкам вверху страницы ↑
    </div>
    <div class="main__title">
      Обо мне:
    </div>
    <div class="main__skills">
      <div class="main__item">
          <a href="mailto:lubabelaya@gmail.com"><svg-icon type="email"></svg-icon>lubabelaya@gmail.com</a>
      </div>
      <div class="main__item">
          <a target="_blank" href="https://spb.hh.ru/resume/7f4510dbff052edd920039ed1f664a78564266"><svg-icon type="id-card"></svg-icon>Резюме на HeadHunter</a>
      </div>
      <div class="main__item">
          <a target="_blank" href="https://github.com/janitor2010"><svg-icon type="github-logo"></svg-icon>Профиль на GitHub</a>
      </div>
    </div>
    </div>
  </section>
</template>

<script>

import svgIcon from '@/components/elements/svg-icon.vue'

export default {
  name: 'app',
  data () {
    return {
      skills: [
        'Python',
        'Linux',
        'Hadoop',
        'MapReduce',
        'Spark',
        'Hive',
        'Tensorflow',
        'Keras',
        'Docker',
        'Git',
        'SQL',
      ]
    }
  },
  methods: {
    randomInt() {
      let arr = [0,1,2,3,4];
      arr.sort(function(a, b){return 0.5 - Math.random()});
      return arr[0];
    }
  },
  components: {
    svgIcon
  },
}
</script>

<style lang="scss" scoped>
  .main {
    &__logo {
      width: 100px;
      height: 100px;
      border-radius: 50px;
      background: $color__accent--green;
      display: inline-block;
    }

    &__title {
      margin-top: 40px;
      text-align: left;
      font-size: 18px;
    }

    &__skills {
      margin-top: 10px;
      display: flex;
      flex-wrap: wrap;

      &-item {
        padding: 5px 10px;
        margin: 5px 5px 0 0;
        color: $color__text--dark;
        background: $color__accent--yellow;

        &-0 {
          background: $color__accent--orange;
        }
        &-1 {
          background: $color__accent--green;
        }
        &-2 {
          background: $color__accent--blue;
        }
        &-3 {
          background: $color__accent--red;
        }
      }
    }

    &__item {
      display: flex;
      align-items: center;
      margin-right: 40px;

      a {
        display: flex;
        align-items: center;

        &:hover svg {
          opacity: .7
        }
      }

      svg {
        font-size: 50px;
        margin-right: 10px;
        color: #fff;
      }
    }
  }
</style>
