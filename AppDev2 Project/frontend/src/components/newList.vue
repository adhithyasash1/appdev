<template>
  <navbar :user_id="this.user_id" />

  <div id='new_list'>
    <div class="mainhead">
      <h1 class="main-heading">
        <span class="main-heading-primary"> Add List </span>
      </h1>
    </div>

    <div class="container">
      <div class='form'>
        <form action="">

          <div class='list_name'>
            <input type="text" placeholder="Name" style="width: 620px;" class="form__field" name='list_name' required v-model="formData.list_name"/>
          </div>

          <div class='list_description'>
            <input type="text" placeholder="Description" style="width: 620px;" class="form__field" name='list_description' required v-model="formData.list_description" />
          </div>

          <div class='submit'>
            <button class="btn" style="color: ghostwhite;" @click.prevent="newList" alt="Submit"> &#10004; </button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";

export default {
  name: "newList",
  inheritAttrs:false,

  components: {
    'navbar': Navbar,
  },

  data() {
    return {
      formData: {
        list_name: '',
        list_description: '',
      },
      user_id: null
    }
  },

  methods: {
    newList() {
      if (this.formData.list_name == null || this.formData.list_description == null) {
        alert('Form data is empty')
      }
      else {
        let data = {
          list_name: this.formData.list_name,
          list_description: this.formData.list_description,
        }
        this.postList(`http://localhost:8080/api/user/list`, data).then((response) => {
          if (response.ok) {
            alert('List created!')
            console.log(response);
            this.$router.push(`/home/${this.user_id}`)
          }
          else {
            console.log('Could not create the list!')
          }
      })}
    },

    async postList(url = '', data = {}) {
      return await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        headers: {
          'user_id': this.user_id,
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Allow-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
      });
    }
  },

  created() {
    this.user_id = this.$route.params.id
  }

};
</script>

<style scoped>
h1 {
  color: saddlebrown;
  text-align: center;
  font-family: monospace;
}

body {
  background-color: ghostwhite;
  font-family: monospace;
}

input[type=text] {
  width: 90%;
  background: transparent;
  border: none;
  padding: 5px 5px;
  border-bottom: 1px solid #000000;
  font-family: monospace;
}


.form__field {
  font-family: inherit;
  width: 100%;
  border: 0;
  border-bottom: 1px solid darkred;
  outline: 0;
  font-size: 16px;
  color: red;
  background: transparent;
  transition: border-color 0.2s;
}

.form__field::placeholder {
  color: red;
  font-family: monospace;
  font-size: 20px;
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
  color: red;
}

.form__field:focus {
  padding-bottom: 6px;
  border-bottom: 2px solid red;
}

.list_name {
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
  display: block;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 3vh;
}


.mainhead {
  position: relative;
  transform: translate(-50%, -50%);
  font-family: monospace;
  left: 755px;
  top: 30px;
}

.main-heading {
  color: saddlebrown;
  text-transform: uppercase;
}

.main-heading-primary {
  display: block;
  font-size: 20px;
  font-family: monospace;
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

.container {
  border-top-left-radius: 37px 140px;
  border-top-right-radius: 23px 130px;
  border-bottom-left-radius: 110px 19px;
  border-bottom-right-radius: 120px 24px;

  display: block;
  position: relative;
  text-align: center;
  border: solid 3px darkred;
  padding: 50px 50px;
  max-width: 700px;
  max-height: 425px;
  width: 60%;
  margin: 10px auto 0;
  font-size: 17px;
  line-height: 25px;
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

.btn {
  background-color: seagreen;
  border: none;
  color: white;
  padding: 12px 16px;
  font-size: 20px;
  font-family: monospace;
  cursor: pointer;
  border-radius: 25px;
  margin-top: 60px;
}

.btn:hover {
  background-color: green;
  font-size: 28px;
}

.new_list {
  align-items: center;
  display: flex;
  justify-content: center;
  align-content: center;
  align-self: center;
}
</style>