<template>
  <div style="width:80%;height:70%;margin:0px auto;;border:2px #cccccc dashed">
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-card bg-variant="light">
        <b-form-group
          label-cols-lg="3"
          label="搶票系統"
          label-size="lg"
          label-class="font-weight-bold pt-0"
          class="mb-0"
        >
          <b-form-group
            id="input-group-1"
            label="homepage"
            label-for="input-1"
            description="設定機器人一開始開出那一個網址。"
          >
            <b-form-input
              id="input-1"
              v-model="form.homepage"
              type="text"
              required
              placeholder="Enter homepage"
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="input-group-2"
            label="ticket_number"
            label-for="input-2"
            description="設定票數"
          >
            <b-form-input
              id="input-2"
              v-model="form.ticket_number"
              required
              placeholder="Enter ticket number"
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="input-group-3"
            label="date_keyword"
            label-for="input-3"
            description="設定日期的關鍵字"
          >
            <b-form-input
              id="input-3"
              v-model="form.date_keyword"
              type="text"
              required
              placeholder="Enter date keyword"
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="input-group-4"
            label="area_keyword"
            label-for="input-4"
            description="設定區域資訊"
          >
            <b-form-input
              id="input-4"
              v-model="form.area_keyword"
              type="text"
              required
              placeholder="Enter area keyword"
            ></b-form-input>
          </b-form-group>
        </b-form-group>
      </b-card>
      <!--<b-form-group id="input-group-3" label="Food:" label-for="input-3">
        <b-form-select id="input-3" v-model="form.food" :options="foods" required></b-form-select>
      </b-form-group>
     

      <b-form-group id="input-group-4">
        <b-form-checkbox-group v-model="form.checked" id="checkboxes-4">
          <b-form-checkbox value="me">Check me out</b-form-checkbox>
          <b-form-checkbox value="that">Check that out</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>
      -->
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        homepage: "",
        ticket_number: "",
        date_keyword: "",
        area_keyword: ""
      },
      foods: [
        { text: "Select One", value: null },
        "Carrots",
        "Beans",
        "Tomatoes",
        "Corn"
      ],
      show: true
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      alert(JSON.stringify(this.form));
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.homepage = "";
      this.form.ticket_number = "";
      this.form.date_keyword = "";
      this.form.area_keyword = "";
      /*this.form.food = null;
      this.form.checked = [];*/
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    }
  }
};
</script>