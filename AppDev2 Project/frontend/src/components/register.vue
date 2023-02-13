<template>
  <div class='header'>
    <h1><p class="p1"> <img src="../assets/logo.webp" width="400" height="198">  </p><br><p class='p3'> Minimal Kanban </p> </h1>
  </div>

  <div class="main">
    <form action="">

      <div class='username'>
        <input type="text" placeholder="Username" class="write" name='username' required v-model="registerData.username"/>
      </div>

      <br>
      <br>

      <div class="email" >
        <input type="email" name="email" class="write" placeholder='Email 📧' v-model="registerData.email" required>
      </div>

      <br>
      <br>

      <div class="password">
        <input type="password" name="password" class="write" placeholder='Password 🔑' v-model="registerData.password" required>
      </div>

      <br>
      <br>
      <br>
      <br>

      <div class='submit'>
        <button class="btnlist" style="color: ghostwhite;" alt="Submit" @click.prevent='newUser'> Register </button>
      </div>

    </form>

  </div>
</template>

<script>
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "register",
  inheritAttrs:false,

  data() {
    return {
      registerData: {
        username: '',
        email: "",
        password: "",
      },
    };
  },

  methods: {
    newUser() {
      if (this.registerData.username == null || this.registerData.email == null || this.registerData.password == null) {
        alert('Form data is empty')
      }
      else {
      let data = {
        username: this.registerData.username,
        email: this.registerData.email,
        password: this.registerData.password,
      };
      this.postUser(`http://localhost:8080/api/user`, data).then((response) => {
          if (response.ok) {
            alert('User created!')
            console.log(response);
            this.$router.push(`/`)
          }
          else {
            console.log(response);
            console.log('Could not create the user!')
          }
        })}
    },

    async postUser(url = '', data = {}) {
      return await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json'
          // 'Authentication-Token': localStorage.getItem('Authentication-Token')
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
      });
    }
  },

}
</script>

<style scoped>
.p2 {
  font-family: monospace;
  font-size: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 10vh;
}
.p3 {
  font-family: monospace;
  font-size: 43px;
  min-height: 10vh;
  color: saddlebrown;
  margin-top: 1px;
}

h1 {
  color: red;
  text-align: center;            }

body {
  font-family: monospace;
  background-color: ghostwhite;
  text-align:center;
}

.main{
  position:relative;
  margin: 100px;
}

.password {
  text-align:center;
}

.email {
  text-align:center;
}

.username {
  text-align:center;
}

textarea, input {
  outline: none;
  border: 0;
  border-bottom: 2px solid green;
  height: 40px;
  width: 50%;
}

input:focus{
  content: "";
}

.submit {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 3vh;

}

/* Style buttons */
.btnlist {
  background-color: seagreen;
  border: none; /* Remove borders */
  color: white; /* White text */
  padding: 12px 16px; /* Some padding */
  font-size: 16px; /* Set a font size */
  cursor: pointer; /* Mouse pointer on hover */
  border-radius: 16px;
  font-family: monospace;
  margin: 10px;
  width: 250px;
}

/* Darker background on mouse-over */
.btnlist:hover {
  background-color: green;
}

.write {
  font-family: monospace;
  font-size: 22px;
}

::placeholder {
  color: saddlebrown;
  opacity: 1;
}
</style>