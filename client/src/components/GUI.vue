<template>
  <div style="width:80%;height:70%;margin:0px auto;;border:20px #cccccc">
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-card bg-variant="light">
        <b-form-group
          label-cols-lg="4"
          label="Tickets grapping system"
          label-size="lg"
          label-class="font-weight-bold pt-0"
          class="mb-0"
        >
          <!--<div>
            <b-img
              left
              v-bind="mainProps"
              src="https://static.tixcraft.com/images/activity/field/19_ERIC_fd102f68892343f323b090bc9e3bbdcf.jpg"
              alt="Left image"
            ></b-img>
            <b-img v-bind="mainProps" blank-color="#777" alt="HEX shorthand color image (#777)"></b-img>
          </div>-->
          <!-- <b-form-group
            id="input-group-1"
            label-cols-sm="3"
            label="入口網址："
            label-for="input-1"
            label-size="lg"
            description="請輸入演唱會購買網址並點選按鈕驗證程式是否抓取到演唱會場次(限拓元售票)"
            label-align-sm="left"
          >
            <b-input-group>
              <b-form-input
                id="input-1"
                v-model="form.homepage"
                type="text"
                required
                placeholder="Enter TixCraft concert URL"
              ></b-form-input>
            </b-input-group>
          </b-form-group>
          <b-form-group label-cols-lg="3" label="使用者登入狀態：" label-size="xm" label-align-sm="left">
            <b></b>
            <b-form-checkbox
              v-model="login"
              size="lg"
              label-checkbox-sm="left"
              name="fail_retry"
              switch
            >
              <b>{{login}}</b>
            </b-form-checkbox>
          </b-form-group>
          -->
          <b-form-group
            id="input-group-1"
            label-cols-sm="3"
            label-align-sm="left"
            label-size="lg"
            label="選擇活動："
            description="請選擇活動(拓元售票)"
            label-for="input-1"
          >
            <b-form-select
              id="input-1"
              v-model="form.ticket_activate"
              :options="activateName"
              required
            ></b-form-select>
          </b-form-group>
          <b-form-group
            id="input-group-2"
            label-cols-sm="2"
            label-align-sm="left"
            label-size="lg"
            label="場次："
            description="請先選擇活動(會自動抓取場次)"
            label-for="input-2"
          >
            <div v-if="isShow">
              <b-form-select
                id="input-2"
                :options="combineSS"
                v-model="form.ticket_session"
                required
              ></b-form-select>
            </div>
            <div v-else>
              <b-spinner variant="primary" label="Text Centered"></b-spinner>
            </div>
          </b-form-group>
          <b-form-group
            id="input-group-3"
            label-cols-sm="3"
            label-align-sm="left"
            label-size="lg"
            label="場域價錢："
            label-for="input-3"
            description="設定要搶的場域的票價"
          >
            <b-form-input
              id="input-3"
              v-model="form.ticket_areaPrice"
              type="number"
              placeholder="請輸入票價"
              required
            ></b-form-input>
          </b-form-group>
          <b-form-group id="picture">
            <div v-if="isShow">
              <b-img-lazy class="my-5" v-bind="mainProps" :src="picture" alt="場域圖"></b-img-lazy>
            </div>
            <div v-else>
              <strong style="text-align:left;">請先選擇活動..</strong>
              <b-spinner variant="primary" type="grow" label="Text Centered"></b-spinner>
            </div>
          </b-form-group>
          <b-form-group
            id="input-group-4"
            label-cols-sm="2"
            label-size="lg"
            label-align-sm="left"
            label="票數："
            label-for="input-4"
            description="設定票數"
          >
            <b-form-input
              id="input-4"
              v-model="form.ticket_number"
              type="number"
              placeholder="請輸入票數"
              required
            ></b-form-input>
          </b-form-group>
          <b-form-group
            label-cols-lg="7"
            label="如果搶票失敗是否由前到後繼續搶票："
            label-size="xm"
            label-align-sm="left"
          >
            <b></b>
            <b-form-checkbox
              v-model="form.fail_retry"
              size="lg"
              label-checkbox-sm="left"
              name="fail_retry"
              switch
            >
              <b>{{form.fail_retry}}</b>
            </b-form-checkbox>
          </b-form-group>
          <div v-if="disable">
            <b-form-input id="input-n" v-model="form.session_index" disabled="false"></b-form-input>
            <b-form-input id="input-urln" v-model="form.activate_URL" disabled="false"></b-form-input>
          </div>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-card>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      activateName: [],
      isShow: false,
      activateURL: [],
      picture: "",
      session: [],
      si: "",
      status: [],
      combineSS: [],
      disable: false,
      list: "",
      form: {
        ticket_activate: "",
        ticket_session: "",
        session_index: "",
        activate_URL: "",
        ticket_areaPrice: "",
        ticket_number: "",
        fail_retry: true
      },
      mainProps: {
        center: true,
        fluidGrow: true,
        blank: true,
        blankColor: "#bbb",
        width: 400,
        height: 200,
        class: "my-5"
      },
      show: true
    };
  },
  created: function() {
    axios
      .get("http://localhost:5000/getActivatyName_URL")
      .then(res => {
        console.log(res);
        console.log(res.data);
        this.activateName = res.data.name;
        this.activateURL = res.data.url;
      })
      .catch(error => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
  computed: {
    isDisabled: function() {
      return !this.login;
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      axios
        .post("http://localhost:5000/getForm", {
          sform: JSON.stringify(this.form)
        })
        .then(res => {
          console.log(res);
        })
        .catch(error => {
          alert("執行失敗");
        });
      //alert(JSON.stringify(this.form));
    },
    onReset(evt) {
      evt.preventDefault();
      this.isShow = false;
      this.form.ticket_activate = "";
      this.form.ticket_session = null;
      this.form.ticket_areaPrice = "";
      this.form.ticket_number = "";
      this.form.fail_retry = true;
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    gstatus() {
      for (var i in this.status) {
        const x = this.status[i];
        return x;
      }
    }
  },
  watch: {
    "form.ticket_activate": function(value) {
      if (value != "") {
        const index = this.activateName.indexOf(this.form.ticket_activate);
        const uUrl = this.activateURL[index];
        this.form.activate_URL = uUrl;
        this.isShow = false;
        console.log(uUrl);
        axios
          .post("http://localhost:5000/useSessionTime", {
            sURL: uUrl
          })
          .then(res => {
            console.log(res);
            if (res.data != null) {
              this.isShow = true;
            }
            this.session = res.data.rSessionTime;
            this.picture = res.data.rPURL;
            this.status = res.data.rstatus;
            this.combineSS = [];
            for (var i = 0; i < this.session.length; i++) {
              var activeSubjectsObject = {};
              for (var j = 0; j < this.status.length; j++) {
                if (i == j) {
                  activeSubjectsObject.value = this.session[i];
                  activeSubjectsObject.text = this.session[i];
                  activeSubjectsObject.disabled = this.status[j];
                  this.combineSS.push(activeSubjectsObject);
                }
              }
            }
            console.log(this.combineSS);
          })
          .catch(error => {
            alert("執行失敗");
          });
      }
    },
    "form.ticket_session": function(value) {
      this.si = this.session.indexOf(this.form.ticket_session);
      this.form.session_index = this.si;
    }
  }
};
</script>
<style>
</style>
