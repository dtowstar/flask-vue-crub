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
            description="請選擇場次(如果沒有抓到場次請重新輸入入口網址)"
            label-for="input-2"
          >
            <b-form-select id="input-2" v-model="form.ticket_session" :options="session" required></b-form-select>
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
      form: {
        ticket_activate: "",
        ticket_session: "",
        ticket_areaPrice: "",
        ticket_number: "",
        fail_retry: true
      },
      session: [],
      show: true
    };
  },
  created: function() {
    axios
      .get("http://localhost:5000/getActivatyName_URL")
      .then(res => {
        console.log(res);
        console.log(res.data);
        this.activateName = res.data;
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
      alert(JSON.stringify(this.form));
    },
    onReset(evt) {
      evt.preventDefault();
      this.form.ticket_activate = "";
      this.form.ticket_session = null;
      this.form.ticket_areaPrice = "";
      this.form.ticket_number = "";
      this.form.fail_retry = true;
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    }
  },
  watch: {
    "form.ticket_activate": function(value) {
      if (value != "") {
        axios
          .post("http://localhost:5000/useSessionTime", {
            activatyName: this.form.ticket_activate
          })
          .then(res => {
            console.log(res);
            this.session = res.data;
          })
          .catch(error => {
            alert("執行失敗");
          });
      }
    }
  }
};
</script>
<style>
</style>
