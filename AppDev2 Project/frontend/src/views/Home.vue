<template>
  <TransitionGroup tag="list" name="bounce" >

  <div class="hasStuff" v-if="lists.length > 0">
    <navbar :user_id="this.user_id" />

    <br>
      <button class="btnlist"><router-link :to="{name: 'newList', params: {id: this.user_id} }" style="color: ghostwhite; text-decoration:none;"> +New List📜 </router-link></button>
      <button class="expBoard" @click.prevent="exportBoard">Export Board</button>

    &nbsp;&nbsp;&nbsp; <button class="impList" @click="submitFile">Import Lists</button>
    &nbsp;&nbsp;&nbsp; <input name="file" id="file" ref="file" type="file" @change="handleFileUpload( $event )" style="font-family: monospace;"/>

    <br>

      <div v-for="list in lists" :key="list.list_id">
        <list :user_id="this.user_id" :list_id="list.list_id" :list_name="list.list_name" :list_description="list.list_description" />
      </div>
  </div>

  </TransitionGroup>

  <TransitionGroup tag="list" name="slide-fade" >
  <div class="noStuff" v-if="lists.length === 0">
    <navbar :user_id="this.user_id" />

    <br>
    <button class="btnlist"><router-link :to="{name: 'newList', params: {id: this.user_id} }" style="color: ghostwhite; text-decoration:none;"> +New List📜 </router-link></button>

    &nbsp;&nbsp;&nbsp;&nbsp;<button class="impList" @click="submitFile">Import Lists</button>
    &nbsp;&nbsp;<input name="file" id="file" ref="file" type="file" @change="handleFileUpload( $event )" style="font-family: monospace;"/>

    <br>
  </div>
  </TransitionGroup>
</template>

<script>
import List from "@/components/List.vue";
import Navbar from "@/components/Navbar.vue";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Home',
  inheritAttrs:false,

  data() {
    return {
      user_id: null,
      lists: [],
      file: null
    }
  },

  methods: {
    exportBoard() {
      this.exportEl('http://localhost:8080/api/user/board/export').then((response) => {
        console.log(response.json());
        if (response.ok) {
          alert('Board exported successfully!')
          window.location.reload();
        }
        else {
          console.log('Could not export the board!')
        }
      })
    },

    async exportEl(url = '') {
      return await fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {
          'user_id': this.user_id,
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Allow-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
      });
    },

    handleFileUpload( event ) {
      this.file = event.target.files[0];
    },

    submitFile() {
      const formData = new FormData();
      formData.append('file', this.file);
      for (let pair of formData.entries()) {
        console.log(pair[0]+ ', ' + pair[1]);
      }
      this.importListsPost('http://localhost:8080/api/user/lists/import', formData).then((response) => {
        console.log(response)
        if (response === 200) {
          alert('Lists imported successfully!')
          window.location.reload();
        } else {
          alert('Could not import lists!')
          console.log('Could not import lists!')
        }
      })
    },

    async importListsPost(url = '', data = {}) {
      const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'user_id': this.user_id,
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
        },
        body: data
      });
      return response.json();
    },

    removeImportListFile( key ){
      this.files.splice( key, 1 );
    }

},

  async mounted() {
    const res = await fetch(`http://localhost:8080/api/user/list`, {
      headers: {
        'user_id' : this.user_id,
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Allow-Control-Allow-Origin': '*',
        'Authentication-Token': localStorage.getItem('Authentication-Token'),
      },
    })
    const data = await res.json()
    if (res.ok) {
      this.lists = data;
    } else if (res.status === 401) {
      console.log(res)
    }
  },

  created() {
    this.user_id = this.$route.params.id
  },

  components: {
    'list': List,
    'navbar': Navbar,
  }
};
</script>

<style>
/* Components Animation Effects */
.bounce-enter-active {
  animation: bounce-in 0.25s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.25);
  }
  100% {
    transform: scale(1);
  }
}

/*
  Enter and leave animations can use different
  durations and timing functions.
*/
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

/* End of Components Animation Effects */


/* Fill button styling for fresh Users */
/* End of Fill Button for fresh Users  */


/* Styling for Existing Users */

.hasStuff {
  font-family: monospace;
  background-color: ghostwhite;
}

.noStuff {
  font-family: monospace;
  background-color: ghostwhite;
}

.btnlist {
  background-color: seagreen;
  border: none;
  color: white;
  padding: 12px 16px;
  font-size: 20px;
  cursor: pointer;
  border-radius: 16px;
  font-family: monospace;
  margin: 10px;
}

.btnlist:hover {
  background-color: green;
}

.option1 {
  float: left;
}

.option2 {
  float: right;
}

.expBoard{
  background-color: #29a1e6;
  border: none;
  color: white;
  padding: 12px 16px;
  font-size: 20px;
  cursor: pointer;
  border-radius: 16px;
  font-family: monospace;
  margin: 10px;
}

.expBoard:hover {
  background-color: hsl(231, 91%, 46%);
}

.impList{
  background-color: saddlebrown;
  border: none;
  color: white;
  padding: 12px 16px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 16px;
  font-family: monospace;
}

.impList:hover {
  background-color: hsl(38, 100%, 50%);
}
/* End of Styling for Existing Users */
</style>
