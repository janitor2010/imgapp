<template>
  <section class="imgapp">
    <div class="imgapp__annotation">
      <div class="layout">
        <span>Задача: </span> Определить класс (из трёх), к которому относится изображение. Для классификации были выбраны изображения картин 3х стилей (Академизм, Абстракционизм, Импрессионизм). Обучающая выборка состояла из 150 изображений.
      </div>
    </div>
    <div class="imgapp__description">
      <div class="layout">Для изображений были выделены специальные характеристики: количество белого цвета,
        сумма контуров изображнения, количество лиц, количество геометрических фигур. Для обучения были протестированы разные алгоритмы:
        RandomForestClassifier, KNeighborsClassifier, DecisionTreeClassifier, LogisticRegression. Наиболее точным (77%) оказался LogisticRegression.
      </div>
    </div>
    <div class="layout">
        <div class="imgapp__title">
            Протестировать:
        </div>
        <div class="imgapp__disclaimer">
          Загрузите фото картины одного из стилей в формате .jpg [Академизм, Абстракционизм, Импрессионизм]

        </div>
        <div class="imgapp__uploading">
          <label class="input-file-label" for="input-file">
              <svg-icon class="icon-upload" type="cloud-computing"></svg-icon>
              <span>Загрузить<br />файл</span>
          </label>
          <input id="input-file" type="file" multiple :name="uploadFieldName" @change="filesChange($event.target.name, $event.target.files);" accept="image/*" class="input-file">
          <div class="imgapp__uploading-text">или</div>
          <div class="imgapp__uploading-link">
              <div class="imgapp__uploading-link-input">
                <input type="text" placeholder="Вставить ссылку" v-model="url" name="" value="">
                <a target="_blank" href="https://goo.gl/FPUa1m">Загуглить изображения</a>
              </div>

              <button @click="sendLink" type="button" name="button">Проверить изображение</button>
          </div>
        </div>
        <div class="imgapp__result">
          <div v-if="pathToImg" :style="resultImgStyle" class="imgapp__result-img">

          </div>
          <div class="imgapp__result-res" v-if="res&&!isUploading&&!isError">Стиль: {{ res }}</div>
          <div class="imgapp__result-res--processing" v-if="isUploading">Обрабатываем изображение...</div>
          <div class="imgapp__result-res--error" v-if="isError">Произошла ошибка, попробуйте с другим файлом</div>
          <table v-if="dataRows.length">
            <tr>
              <th>Изображение</th>
              <th>Процент белого цвета</th>
              <th>Количество лиц</th>
              <th>Общая ширина контуров</th>
              <th>Количество небольших объектов</th>
              <th>Результат</th>
            </tr>
            <tr v-for="row in dataRows">
              <td><img :src="row.imgPath" /></td>
              <td>{{ row.white }}</td>
              <td>{{ row.faces }}</td>
              <td>{{ row.edges }}</td>
              <td>{{ row.smalls }}</td>
              <td>{{ row.class }}</td>
            </tr>
          </table>
        </div>

    </div>
    <div class="imgapp__bottom">
      <a target="_blank" href="https://github.com/janitor2010"><svg-icon type="github-logo"></svg-icon></a>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import svgIcon from '@/components/elements/svg-icon.vue'

export default {
  name: 'app',
  data () {
    return {
      msg: 'Upload file, bitch! (jpg)',
      uploadFieldName: 'files',
      url: '',
      pathToImg: '',
      res: '',
      isUploading: false,
      isError: false,
      imageUrl: '/static/up/01.jpg',
      dataRows: []
    }
  },
  methods: {
    filesChange(fieldName, fileList) {
      console.log("changes",fieldName,fileList);
      const formData = new FormData();

      if (!fileList.length) return;
      let host = this;

      host.pathToImg = '';
      host.isUploading = true;
      host.isError = false;
      host.url = '';
      Array
        .from(Array(fileList.length).keys())
        .map(x => {
          formData.append(fieldName, fileList[x], fileList[x].name);
        });
        const path = `/random`
        axios.post(path, formData)
          // get data
          .then(x => {
            console.log("res",x);
            host.isUploading = false;
            host.res = x.data.class;
            host.pathToImg = x.data.path;
            x.data.info['imgPath'] = host.pathToImg;
            x.data.info['class'] = host.res;
            host.dataRows.push(x.data.info)

          }).catch(function (error) {
              host.isUploading = false;
              host.isError = true;
              console.log(error);
          })

    },
    goGet() {
      const path = `/random`
      axios.get(path);
    },
    handleAvatarSuccess() {},
    beforeAvatarUpload() {},
    sendLink() {
      let host = this;

      host.pathToImg = '';
      host.isUploading = true;
      host.isError = false;

      const path = `/file-by-url`
      axios.post(path, { url: this.url })
        // get data
        .then(x => {
          console.log("res",x);
          host.isUploading = false;
          host.res = x.data.class;
          host.pathToImg = x.data.path;
          x.data.info['imgPath'] = host.pathToImg;
          x.data.info['class'] = host.res;
          host.dataRows.push(x.data.info)
        }).catch(function (error) {
            host.isUploading = false;
            host.isError = true;
            console.log(error);
        })
    }
  },
  computed: {
    pathToI() {
      if (this.pathToImg) {
        return (this.pathToImg).substring(52);
      }
      else return '';
    },
    resultImgStyle() {
      return {
        backgroundImage: 'url('+this.pathToImg+')'
      }
    }
  },
  components: { svgIcon }
}
</script>
<style lang="scss" scoped>





</style>
