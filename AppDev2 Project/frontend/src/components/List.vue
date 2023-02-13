<template>
  <div class="container">

    <h1>📌{{ this.list_name }}</h1>
    <h4> {{ this.list_description }}</h4>


      <div v-for="card in cards" :key="card.card_id">
        <card :user_id="this.user_id" :list_id='this.list_id' :card_id="card.card_id" :card_title="card.card_title" :card_content="card.card_content" :card_status="card.card_status" :card_deadline="card.card_deadline"/>
        <div class="option1"><button class="editCard"><router-link :to="{ name: 'updateCard', params: { id: this.user_id, list_id: this.list_id, card_id: card.card_id } }"> ✏️ </router-link></button></div>
        <div class="option2"><button class="deleteCard" @click="deleteCardTrigger(card.card_id)"> &#9940; </button></div>
      </div>

    <br>
    <br>
    <br>
    <p style="text-align: center;"><button class="btncard"><router-link :to="{name: 'newCard', params: {id: this.user_id, list_id: this.list_id} }" style="color: ghostwhite; text-decoration:none;"> +New Card </router-link></button></p>
    <br>

    <br>
    <button class="upList"><router-link :to="{ name: 'updateList', params: { id: this.user_id, list_id: this.list_id } }" style="color: black; text-decoration:none; font-family: monospace; border: none;">Edit List</router-link></button>
    <button class="delList" @click.prevent="deleteList">Delete List</button>

    <br>
    <br>
    <button class="expList" v-if="trans" @click="exportBoard"> Export </button>
    <button class="delList" v-if="trans"><router-link :to="{ name: 'transferCards', params: { id: this.user_id, list_id: this.list_id } }" style="color: whitesmoke; text-decoration:none; font-family: monospace">Transfer and Delete </router-link></button>
    <br>
    <br>
    &nbsp;&nbsp;&nbsp; <button class="impCards" @click="submitCard">Import Cards</button>
    &nbsp;&nbsp;&nbsp; <input type="file" @change="handleCardFileUpload( $event )" style="font-family: monospace;"/>

  </div>
</template>

<script>
import Card from "@/components/Card.vue";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "List",
  inheritAttrs:false,

  props: {
      list_id: null,
      list_name: null,
      list_description: null,
      user_id: null,
  },

  components: {
    'card' : Card,
  },

  methods: {
    deleteList: async function ( data = {}) {
      return await fetch('http://localhost:8080/api/user/list', {
        method: 'DELETE',
        headers: {
          'user_id': this.user_id,
          'list_id': this.list_id,
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
      }).then((response) => {
        console.log(response);
        if (response.ok) {
          alert('List deleted successfully!')
          console.log(data);
          window.location.reload();
        } else {
          console.log(response);
          console.log('Could not delete the list!')
        }
      })
    },

    deleteCard: async function (url = 'http://localhost:8080/api/user/list/card') {
      return await fetch(url, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
          'user_id': this.user_id,
          'card_id': this.cardToDelete,
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          // 'Content-Type': 'application/x-www-form-urlencoded',
        }
      }).then((response) => {
        console.log(response);
        if (response.ok) {
          alert('Card deleted successfully!')
          console.log(response);
          // window.location.reload();
        } else {
          console.log(response);
          console.log('Could not delete the card!')
        }
      })
    },

    deleteCardTrigger: function (x) {
      this.cardToDelete = x;
      this.deleteCard();
      window.location.reload();
    },

    exportBoard() {
      this.exportLi('http://localhost:8080/api/user/list/export').then((response) => {
        console.log(response.json());
        if (response.ok) {
          alert('List exported successfully!')
          window.location.reload();
        }
        else {
          console.log('Could not export the list!')
        }
      })
    },

    async exportLi(url = '') {
      console.log(this.user_id, this.list_id);
      return await fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {
          'user_id': this.user_id,
          'list_id': this.list_id,
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Allow-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
      });
    },

    handleCardFileUpload( event ) {
      this.file = event.target.files[0];
    },

    submitCard() {
      const formData = new FormData();
      formData.append('file', this.file);
      for (let pair of formData.entries()) {
        console.log(pair[0]+ ', ' + pair[1]);
      }
      this.importCardsPost('http://localhost:8080/api/user/list/cards/import', formData).then((response) => {
        console.log(response)
        if (response === 200) {
          alert('Cards imported successfully!')
          window.location.reload();
        } else {
          alert('Could not import lists!')
          console.log('Could not import cards!')
        }
      })
    },

    async importCardsPost(url = '', data = {}) {
      const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'user_id': this.user_id,
          'list_id': this.list_id,
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
        },
        body: data
      });
      return response.json();
    },

    removeImportCardFile( key ){
      this.files.splice( key, 1 );
    }
  },

  data() {
    return {
      cards: null,
      cardToDelete: null,
      trans: null
    }
  },

  async mounted() {
    const res = await fetch(`http://localhost:8080/api/user/list/card`, {
      headers: {
        'user_id' : this.user_id,
        'list_id' : this.list_id,
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': localStorage.getItem('Authentication-Token'),
      },
    })
    const data = await res.json()
    if (res.ok) {
      this.cards = data;
      if (this.cards !== null) {
        this.trans = true;
      }
    }
    else if (res.status === 401) {
      this.error = data.response.error
    }
    else {
      this.error = data.message
    }
  },


}
</script>

<style scoped>

.btnlist {
  background-color: seagreen;
  border: none; /* Remove borders */
  color: white; /* White text */
  padding: 12px 16px; /* Some padding */
  font-size: 20px; /* Set a font size */
  cursor: pointer; /* Mouse pointer on hover */
  border-radius: 16px;
  font-family: monospace;
  margin: 10px;
}

/* Darker background on mouse-over */
.btnlist:hover {
  background-color: green;
}

/* Style buttons */
.btncard {
  background-color: seagreen;
  border: none; /* Remove borders */
  color: white; /* White text */
  padding: 12px 16px; /* Some padding */
  font-size: 16px; /* Set a font size */
  cursor: pointer; /* Mouse pointer on hover */
  border-radius: 16px;
  font-family: monospace;

}

/* Darker background on mouse-over */
.btncard:hover {
  background-color: green;
}

.container {
  border-top-left-radius: 37px 140px;
  border-top-right-radius: 23px 130px;
  border-bottom-left-radius: 110px 19px;
  border-bottom-right-radius: 120px 24px;

  display: block;
  position: relative;
  border: solid 3px darkred;
  padding: 20px 40px;
  max-width: 800px;
  width: 16rem;
  margin: 120px auto 0;
  margin-left: 25px;
  font-size: 17px;
  font-family: monospace;
  line-height: 28px;
  transform: rotate(-1deg);
  box-shadow: 3px 15px 8px -10px rgba(0, 0, 0, 0.3);
  transition: all 0.13s ease-in;
  float: left;
  margin-top: 15px;
}

.container:hover {
  transform: translateY(-10px) rotate(1deg);
  box-shadow: 3px 15px 8px -10px rgba(0, 0, 0, 0.3);
}

.container:hover .border {
  transform: translateY(4px) rotate(-5deg);
}

.border {
  position: absolute;
  transition: all 0.13s ease-in;
}

.border:before,
.border:after {
  color: #515d9c;
  font-size: 15px;
  position: absolute;
}

.tl {
  position: absolute;
  left: -50px;
  top: -63px;
  font-weight: 600;
}

.tl:before {
  content: "37px";
  left: 120px;
  top: 30px;
}

.tl:after {
  content: "140px";
  left: 0px;
  top: 80px;
}

.tr {
  right: -50px;
  top: -63px;
  font-weight: 600;
}

.tr:before {
  content: "23px";
  left: 0;
  top: 30px;
}

.tr:after {
  content: "130px";
  left: 130px;
  top: 80px;
}

.bl {
  left: -50px;
  bottom: -71px;
  font-weight: 600;
}

.bl:before {
  content: "110px";
  left: 120px;
  top: -30px;
}

.bl:after {
  content: "19px";
  left: 0px;
  top: -90px;
}

.br {
  right: -50px;
  bottom: -63px;
  font-weight: 600;
}

.br:before {
  content: "120px";
  left: 0;
  top: -30px;
}

.br:after {
  content: "24px";
  right: -10px;
  top: -80px;
}

pre {
  background: #edeff5;
  padding: 20px;
}

.option1 {
  float: left;
  border: none;
  color: white;
  padding: 10px 12px;
  cursor: pointer;
  border-radius: 18px;
}

.option2 {
  float: right;
  border: none;
  color: white;
  padding: 10px 12px;
  cursor: pointer;
  border-radius: 18px;
}

.delList {
  float: right;
  background-color: hsl(0, 100%, 35%);
  color: whitesmoke;
  border-radius: 10px;
  padding: 8px;
  border: none;
  font-family: monospace;
}

.delList:hover {
  background-color: hsl(0, 100%, 40%)
}

.deleteCard {
  float: right;
  background-color: hsl(0, 88%, 63%);
  border: 2px, dotted;
  border-radius: 12px;
  padding: 8px;
  font-family: monospace;
}

.deleteCard:hover {
  background-color: hsl(0, 98%, 41%)
}

.upList {
  background-color: #BD850DFF;
  border-radius: 10px;
  padding: 8px;
  border: none;
}

.upList:hover {
  background-color: #CC6300FF;
}

.editCard {
  background-color: #BD850DFF;
  border: 2px, dotted;
  border-radius: 12px;
  padding: 8px;
}

.editCard:hover {
  background-color: #CC6300FF;
}

.expList{
  background-color: hsl(202, 79%, 53%);
  border: none;
  border-radius: 10px;
  padding: 10px;
  font-family: monospace;
  color: white;
  font-size: 15px;
}

.expList:hover {
  background-color: hsl(231, 91%, 46%);
}

.impCards{
  background-color: #4cff67;
  border: none;
  color: darkgreen;
  padding: 12px 16px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 16px;
  font-family: monospace;
}

.impCards:hover {
  background-color: hsl(120, 40%, 74%);
}
</style>