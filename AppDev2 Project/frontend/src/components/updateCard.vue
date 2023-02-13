<template>
  <navbar :user_id="this.user_id" />

  <div class="mainhead">
    <h1 class="main-heading">
      <span class="main-heading-primary"> Update Card </span>
    </h1>
  </div>

  <div class="container">
    <div class='form'>

      <form action="">

        <div class='list_name'>
          <select name='card_list_id'  v-model="formData.card_list_id"  class="form__field" required style="width:620px;">
            <option v-for="list in lists" :key="list.list_id" :value="list.list_id">> {{ list.list_name }} </option>
          </select>
        </div>

        <br>
        <br>

        <div class='card_title'>
          <input type="text" placeholder="Card Title" class="form__field" name='card_title' required style="width:620px;" v-model="formData.card_title"/>
        </div>

        <br>
        <br>

        <div class='card_content'>
          <input type="text" placeholder="Card Content" class="form__field" name='card_content' required style="width:620px;" v-model="formData.card_content"/>
        </div>

        <br>
        <br>

        <div class='card_deadline'>
          <input type="datetime-local" class="form__field" name="card_deadline" min="1970-06-07T00:00" max="2100-06-14T00:00" placeholder="🚨Card Deadline" required style="width:620px;" v-model="formData.card_deadline"/>
        </div>

        <br>
        <br>

        <div class='card_status'>
          <select name='card_status' v-model="formData.card_status" class="form__field" required style="width:620px;">
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
            <option value="Past Deadline">Past Deadline</option>
          </select>
        </div>

        <br>
        <br>

        <div class='submit'>
          <button class="btn" style="color: ghostwhite;" @click.prevent="updateCard" alt="Submit"> &#10004; </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import {router} from "@/router/router";

export default {
  name: "updateCard",
  inheritAttrs:false,

  components: {
    'navbar': Navbar,
  },

  data() {
    return {
      formData: {
        card_status: '',
        card_title: '',
        card_content: '',
        card_deadline: '',
        card_list_id: ''
      },
      user_id: null,
      list_id: null,
      card_id: null,
      lists: null
    }
  },

  methods: {
    updateCard() {
      if (this.formData.card_title == null || this.formData.card_content == null || this.formData.card_deadline == null || this.formData.card_status == null) {
        alert('Form data is empty')
      }
      else {
        let data = {
          card_status: this.formData.card_status,
          card_title: this.formData.card_title,
          card_content: this.formData.card_content,
          card_deadline: this.formData.card_deadline,
          card_list_id: this.formData.card_list_id
        }
        console.log(data);
        this.putCard(`http://localhost:8080/api/user/list/card`, data).then((response) => {
          console.log(response)
          if (response.ok) {
            alert('Card updated!')
            console.log(response);
            router.push(`/home/${this.user_id}`)
          }
          else {
            console.log('Could not update the card!')
          }
      })}
    },

    async putCard(url = '', data = {}) {
      return await fetch(url, {
        method: 'PUT',
        mode: 'cors',
        headers: {
          'user_id': this.user_id,
          'list_id': this.list_id,
          'card_id': this.card_id,
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
      });
    }
  },

  async mounted() {
    const res = await fetch(`http://localhost:8080/api/user/list`, {
      headers: {
        'user_id' : this.user_id,
        'Content-Type': 'application/json',
        'Allow-Control-Allow-Origin': '*',
        'Access-Control-Allow-Origin': '*',
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
    this.user_id = this.$route.params.id,
    this.list_id = this.$route.params.list_id,
    this.card_id = this.$route.params.card_id
  }
}
</script>

<style scoped>
h1 {
  font-family: monospace;
  color: saddlebrown;
  text-align: center;
}

body {
  background-color: ghostwhite;
  font-family: monospace;
}

input[type=text] {
  width: 40%;
  background: transparent;
  border: none;
  padding: 2px 5px;
  border-bottom: 1px solid #000000;
  font-family: monospace;
}


.form__field {
  font-family: monospace;
  width: 100%;
  border: 0;
  border-bottom: 1.2px solid darkred;
  outline: 0;
  font-size: 16px;
  color: red;
  padding: 7px 0;
  background: transparent;
  transition: border-color 0.2s;
}

.form__field::placeholder {
  color: red;
  font-family: monospace;
}

.form__field:placeholder-shown ~ .form__label {
  font-size: 16px;
  cursor: text;
  top: 20px;
}

label,
.form__field:focus ~ .form__label {
  position: absolute;
  top: 0;
  display: block;
  transition: 0.2s;
  font-size: 12px;
  color: red;
}

.form__field:focus ~ .form__label {
  color: darkred;
}

.form__field:focus {
  padding-bottom: 6px;
  border-bottom: 2px solid saddlebrown;
}

.username {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 20vh;
  color: red;
  padding: 25px 20px;
  margin: 8px 0;
  box-sizing: border-box;

}

.submit {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 3vh;
}

.form {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.container {
  border-top-left-radius: 37px 140px;
  border-top-right-radius: 23px 130px;
  border-bottom-left-radius: 110px 19px;
  border-bottom-right-radius: 120px 24px;

  display: block;
  position: relative;
  text-align: center;
  border: solid 3px darkred;
  padding: 50px 60px;
  max-width: 700px;
  max-height: 325px;
  width: 60%;
  margin: 60px auto 0;
  font-size: 17px;
  line-height: 15px;
  transform: rotate(-1deg);
  box-shadow: 3px 15px 8px -10px rgba(0, 0, 0, 0.3);
  transition: all 0.13s ease-in;
  margin-left: 339px;
  margin-top: 37px;
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

/* Style buttons */
.btn {
  background-color: seagreen;
  border: none; /* Remove borders */
  color: white; /* White text */
  padding: 16px 20px; /* Some padding */
  font-size: 16px; /* Set a font size */
  cursor: pointer; /* Mouse pointer on hover */
  border-radius: 46px;
  width: 60px;
  height: 60px;
}

/* Darker background on mouse-over */
.btn:hover {
  background-color: green;
  font-size: 28px;
}

.mainhead {
  position: relative;
  transform: translate(-50%, -50%);
  font-family: monospace;
  left: 770px;
  top: 30px;
}

.main-heading {
  font-family: monospace;
  color: saddlebrown;
  text-transform: uppercase;
}

.main-heading-primary {
  font-family: monospace;
  display: block;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 15px;
  animation: moveInLeft 1s ease-out;
}

@keyframes moveInLeft {
  0% {
    opacity: 0;
    transform: translateX(-100px);
  }

  80% {
    transform: translateX(10px);
  }

  100% {
    opacity: 1;
    transform: translate(0);
  }
}

@keyframes moveInRight {
  0% {
    opacity: 0;
    transform: translateX(100px);
  }

  80% {
    transform: translateX(-10px);
  }

  100% {
    opacity: 1;
    transform: translate(0);
  }
}
</style>