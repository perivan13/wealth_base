<template>
  <div id="edit-form">
    <div style="position: absolute; z-index: 999; width: 99%; margin: auto">
      <b-alert :show="success" dismissible variant="success">
        <p style="text-align: center;">
          <b-icon icon="check2"
                  variant="success"
                  font-scale="1"
                  data-toggle="tooltip"
                  data-placement="top">
          </b-icon>
          Успешно <a href="#/items/">Вернуться на главную</a>
        </p>
      </b-alert>
    </div>
    <b-row class="mt-3">
      <b-col cols="2">
        <div id="scrollspy-buttons"
             :style="{ height: scroll_form }"
             ref="buttons">
          <b-button variant="success"
                    v-b-modal.confirm-modal>
            Внести изменения
          </b-button>
          <b-navbar v-b-scrollspy:scrollspy-nested class="flex-column">
            <b-nav pills vertical>
              <b-nav-item v-for="item in itemsForEdit"
                          :key="item['_id']"
                          :href="'#item-' + item['_id']"
                          @click="scrollIntoView">
                <div>
                  {{ item.name ? item.name : 'Материальная ценность ' + (item.index + 1) }}
                </div>
              </b-nav-item>
            </b-nav>
          </b-navbar>
        </div>
      </b-col>
      <b-col cols="10">
        <div id="scrollspy-nested"
             :style="{ height: scroll_form }"
             ref="items">
          <group-edit-form v-for="item in itemsForEdit"
                           :key="item['_id']"
                           :itemForm="item"
                           :id="'item-' + item['_id']"
                           :employeeInitials="employeeInitials"/>
        </div>
      </b-col>
    </b-row>
    <confirm-form :message="message"
                  :payload="itemsForEdit"
                  dynamic-id="confirm-modal"
                  :op="editItems"/>
  </div>
</template>

<script>
/* eslint-disable */
  import GroupEditForm from "./GroupEditForm";
  import {bus} from "../../../../main";
  import ConfirmForm from "../../ConfirmForm";

  export default {
    name: "GroupEditPage",
    components: {
      GroupEditForm,
      ConfirmForm
    },
    data() {
      return {
        employeeInitials: [],
        disableEdit: true,
        scroll_form: '',
        employeeList: [],
        itemsForEdit: [],
        m: '',
        success: false,
        prep_employees: []
      }
    },
    methods: {
      employeeToString() {
        for (let i = 0; i < this.employeeList.length; i++) {
          this.employeeInitials.push(
            this.employeeList[i].surname + ' ' +
            this.employeeList[i].name[0] + '.' +
            this.employeeList[i].secname[0] + '.');
        }
      },
      async fetchEmployees() {
        const response = await fetch(`${process.env.ROOT_API}/inventorybase/api/v1/employee/`,
        {
          mode: "cors",
        })
        this.employeeList = await response.json()
        this.prep_employees = this.employeeList['prep_employees']
        this.employeeList = this.employeeList['employees']
        this.employeeToString()
      },
      scrollIntoView(evt) {
        evt.preventDefault()
        const href = evt.target.getAttribute('href')
        const el = href ? document.querySelector(href) : null
        if (el) {
          this.$refs.items.scrollTop = el.offsetTop
        }
      },
      async editItems() {
        for (let i = 0; i < this.itemsForEdit.length; i++) {
          const _id = this.itemsForEdit[i]['_id']
          const response = await fetch(`${process.env.ROOT_API}/inventorybase/api/v1/item/${_id}/`,
            {
              method: 'PUT',
              mode:'cors',
              body: JSON.stringify(this.itemsForEdit[i]),
              headers: {
                'Accept': 'application/json',
                'Content-type': 'application/json'
              },
            });
          const json = await response.json();
          console.log(JSON.stringify(json));
          if (response.status !== 202) {
            alert(JSON.stringify(await response.json(), null, 2));
          }
        }
        this.success = true
      },
    },
    computed:{
      message: function () {
        if(this.itemsForEdit) {
          if (this.itemsForEdit.length === 1) {
            this.m = 'Вы уверены, что хотите внести изменения в запись?'
          } else {
            this.m = 'Вы уверены, что хотите внести изменения в записи?'
          }
        }
        return this.m
      }
    },
    async created() {
      await this.fetchEmployees()
      this.itemsForEdit = this.$parent.$data.dataForChildren
      bus.$emit('clearDataForChildren')
      this.success = false
    },
    mounted() {
      let _height = document.documentElement.clientHeight * 0.9
      this.scroll_form = _height.toString() + 'px'
    }
  }
</script>

<style scoped>
  #scrollspy-nested{
    position:relative;
    width: 98%;
    overflow-y: scroll;
    overflow-x: scroll;
  }
  #edit-form{
    width: 99%;
    margin: auto;
    overflow-x: scroll;
  }
  #scrollspy-buttons{
    position:relative;
    overflow-y:scroll;
    white-space: normal;
    width: 105%;
    overflow-x: scroll;
  }
</style>
