<!-- eslint-disable -->
<template>
  <b-modal id="edit-item-modal"
           ref="editItemModal"
           title="Изменить запись в базе мат. ценностей"
           size="xl"
           no-close-on-backdrop
           @hidden="clearForm"
           @show="clearForm"
           hide-footer>
    <!--no-close-on-backdrop или настроить очистку формы при нажатии на задний фон-->

    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <div class="submit-reset-buttons mt-3">
        <b-button type="submit"
                  :disabled="itemForm.name === ''"
                  variant="primary">
          Изменить запись
        </b-button>
        <!--        @click="initForm"-->
        <b-button type="reset" variant="danger">Отмена</b-button>

        <b-button id="add-component-button"
                  @click="showComponents = !showComponents">
          Изменить компоненты
        </b-button>
      </div>
      <b-container class="mt-3">
        <b-row>
          <b-col :cols="colsize">
            <form-template :itemForm="itemForm"
                           :categories="categories"
                           :show-components="showComponents"
                           :location_objects="location_objects"
                           :location_corpuses="location_corpuses"
                           :location_cabinets="location_cabinets"
                           :employeeInitials="employeeInitials"></form-template>
          </b-col>
          <b-col>
            <b-card v-if="showComponents"
                    no-body
                    class="mt-3">
              <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller>
                <b-nav-item @click="scrollIntoView"
                            v-for="component in itemForm['components']"
                            :key="component.id"
                            :href="'#component'+component.id">
                  {{ component.name ? component.name : 'Компонент ' + (component.id + 1) }}
                </b-nav-item>
              </b-nav>

              <b-card-body
                id="nav-scroller"
                ref="content"
                style="position:relative; overflow-y:scroll;">
                <component-card ref="componentCard"
                                v-for="component in itemForm['components']"
                                :key="component.id"
                                :components="itemForm['components']"
                                :component="component"/>
                <b-row>
                  <b-col cols="6">
                    <b-button @click="addComponent"
                              variant="primary">
                      Добавить компонент
                    </b-button>
                  </b-col>
                  <b-col cols="6">
                    <b-button v-if="itemForm['components'].length > 0"
                              variant="danger"
                              @click="deleteLastComponent">
                      Удалить компонент
                    </b-button>
                  </b-col>
                </b-row>
              </b-card-body>
            </b-card>
          </b-col>
        </b-row>
      </b-container>
    </b-form>
  </b-modal>
</template>

<script>
/* eslint-disable */
  import ComponentCard from "./ComponentCard";
  import FormTemplate from "../FormTemplate";

  export default {
    name: 'editModal',
    props: ['employeeInitials',
      'editItem',
      'categories',
      'location_objects',
      'location_corpuses',
      'location_cabinets'],
    components: {
      ComponentCard,
      FormTemplate
    },
    data() {
      return {
        itemForm: {
          components: []
        },
        index: 0,
        showComponents: false
      }
    },
    computed:{
      colsize: function(){
        if(this.showComponents)
          return 6
        else
          return 12
      }
    },
    methods: {
      onReset(evt) {
        evt.preventDefault();
        this.$refs.editItemModal.hide();
      },
      onSubmit(evt) {
        evt.preventDefault();
        this.$refs.editItemModal.hide();
        // this.itemForm.components = this.$refs.componentScrollableList.createComponentList()
        const payload = this.itemForm
        this.editItem(payload)
      },
      scrollIntoView(evt) {
        evt.preventDefault()
        const href = evt.target.getAttribute('href')
        const el = href ? document.querySelector(href) : null
        if (el) {
          this.$refs.content.scrollTop = el.offsetTop
        }
      },
      addComponent(){
        let componentForm = {
          id: this.index,
          name: '',
          serial_n: '',
          category: '',
          type: '',
          year: '',
          cost: '',
          location: {
            object: '',
            corpus: '',
            cabinet: '',
          },
          user: '',
          in_operation: '',
          condition: ''
        }
        this.itemForm.components.push(componentForm)
        this.index += 1
      },
      deleteLastComponent(){
        this.itemForm.components.splice( this.itemForm.components.length-1, 1)
        this.index -= 1
      },
      showComponentForm(){
        if(!this.showComponents){
          this.showComponents = true
          this.addComponent()
        } else {
          this.showComponents = false
          this.deleteLastComponent()
          this.index = 0
        }
      },
      clearForm(){
        this.index = 0
        this.showComponents = false
      }
    },
  };
</script>

<style scoped>
  .add-component {
    display: flow;
  }
  .card {
    height: 1105px;
  }
  #add-component-button {
    position: absolute;
    right: 1.5%;
  }
</style>
