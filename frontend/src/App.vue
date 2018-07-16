<template>
  <section class="section-main">
    <div class="wrapper-main">
      <div class="title">{{ msg }}</div>
      <div class="disclaimer">
        Пытается11 распознать один из трёх стилей<br>[Академизм, Абстракционизм, Импрессионизм]<br>можно загуглить и взять любую картинку из этих стилей
      </div>
      <form class="form-main" action="index.html" method="post">
        <input type="file" multiple :name="uploadFieldName" @change="filesChange($event.target.name, $event.target.files);" accept="image/*" class="input-file">
      </form>
      <img class="img-main" v-if="pathToI&&!isUploading&&!isError" :src="pathToI">
      <div class="answer-main" v-if="res&&!isUploading&&!isError">Стиль: {{ res }}</div>
      <div class="answer-main" v-if="isUploading">Processing file...</div>
      <div class="answer-main" v-if="isError">Smth fucked up, try another file</div>
      <!--<div @click="goGet">ffffff</div>-->
    </div>

  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data () {
    return {
      msg: 'Upload file, bitch! (jpg)',
      uploadFieldName: 'files',
      pathToImg: '',
      res: '',
      isUploading: false,
      isError: false,
    }
  },
  methods: {
    filesChange(fieldName, fileList) {
      console.log("changes",fieldName,fileList);
      const formData = new FormData();

      if (!fileList.length) return;
      let host = this;
      // append the files to FormData

      host.isUploading = true;
      host.isError = false;
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
            host.res = x.data.res;
            host.pathToImg = x.data.path;
          }).catch(function (error) {
              host.isUploading = false;
              host.isError = true;
              console.log(error);
          })

    },
    goGet() {
      const path = `/random`
      axios.get(path);
    }
  },
  computed: {
    pathToI() {
      if (this.pathToImg) {
        return (this.pathToImg).substring(52);
      }
      else return '';
    }
  }
}
</script>
<style lang="scss">
  body {
    font-size: 16px;
    font-family: 'Raleway', sans-serif;
    background: url('assets/bg.jpg')no-repeat center; //
    margin: 0;

    .section-main {
      display:flex;
      align-items:center;
      justify-content: center;
      height:100vh;

      .wrapper-main {
        background: rgba(255,255,255,.8);
        padding: 50px;
        max-width:500px;

        @media all and (max-width: 600px) {
              max-width:100%;
              padding:20px;
          }

        .title {
          font-size:2rem;
          text-align: center;

          @media all and (max-width: 600px) {
                font-size:1.7rem;
            }
        }

        .disclaimer {
            font-size: .8rem;
            margin-bottom:40px;
            text-align: center;

            @media all and (max-width: 600px) {
              font-size: .9rem;
            }
        }

        .answer-main {
          margin-top:20px;
        }

        .form-main {
          margin-bottom:20px;
        }
        .img-main {
          width:300px;
        }
      }

      .bottom-disclaimer {
        font-size: .9rem;
        padding: 10px;
        background: rgba(255,255,255,.8);
        position: absolute;
        bottom: 30px;
        left:0;
        right:0;
        margin: auto;
        text-align: center;
      }
    }
  }


</style>
