<template>
  <div class='header'>
    <h1><p class="p1"> <img alt="logo" src="../assets/logo.webp" width="400" height="198">  </p><br><p class='p3'> Minimal Kanban </p> </h1>
  </div>

  <div class="main">
    <form action="">

      <div class="email" >
        <input type="email" name="email" class="write" placeholder='Email 📧' required v-model="loginData.email"/>
      </div>

      <br>
      <br>

      <div class="password">
        <input type="password" name="password" class="write" placeholder='Password 🔑' required v-model="loginData.password"/>
       </div>

        <br>
        <br>
        <br>
        <br>

      <div class='submit'>
       <button class="btnlist" style="color: ghostwhite;" @click.prevent='loginUser'> Login </button>
      </div>

      </form>
  </div>

  <div>
    <p class="p2"> Don't have an account? <router-link to="/register"> Register </router-link> </p>
  </div>

</template>

<script>
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "login",

  data() {
    return {
      loginData: {
        email: "",
        password: "",
      },

      user_id: null,
      username: null,
      email: null,
    };
  },

  methods: {
    async loginUser() {
      const res = await fetch(`http://localhost:8080/login?include_auth_token`, {
        method: 'POST',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Allow-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
        },
        body: JSON.stringify(this.loginData),
      })

      if (res.ok) {
        const data = await res.json()
        localStorage.setItem(
            'Authentication-Token',
            data.response.user.authentication_token
        )
        this.user_id = data.response.user.id
        this.username = data.response.user.username
        this.email = data.response.user.email
        this.$router.push(`/home/${this.user_id}`)
      } else {
        console.log(res);
        console.log('Something Went Wrong!')
      }
    },
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