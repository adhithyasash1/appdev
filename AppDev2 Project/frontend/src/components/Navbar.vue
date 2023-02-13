<template>
  <div class="navbar">
    <img class='logo' src='../assets/logo.webp' width=100 height=50 alt="logo">

    <div class="dropdown">
      <button class="dropbtn">
        Profile🔻
        <i class="down"></i>
      </button>
      <div class="dropdown-content">
        <a> {{ username }} </a>
        <router-link :to="{ name: 'Home', params: { id: this.user_id } }"> Home 🛸</router-link>
        <router-link :to="{ name: 'Summary', params: { id: this.user_id } }"> Summary &#x1f4ca;</router-link>
        <a href="" @click.prevent="logout"> Logout </a>
      </div>
    </div>

  </div>
</template>

<script>
import logout from "@/functions/logout.js";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Navbar",
  inheritAttrs: false,

  methods: {
    logout() {
      logout();
    },
  },

  props: {
    user_id: null,
  },

  data() {
    return {
      username: null
    };
  },

  async mounted() {
    const res = await fetch(`http://localhost:8080/api/identification`, {
      headers: {
        'user_id': this.user_id,
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Allow-Control-Allow-Origin': '*',
        'Authentication-Token': localStorage.getItem('Authentication-Token'),
      },
    })
    const data = await res.json()
    if (res.ok) {
      console.log(data);
      this.username = data.username;
      console.log(data.username);
    } else if (res.status === 401) {
      console.log(res)
    }
  },
}
</script>

<style scoped>
/* Navbar */
.logo {
  float: left;
  margin-left: 10px;
  margin-top: 10px;
}

.navbar {
  overflow: hidden;
  background-color: ghostwhite;
  font-family: monospace;
}

.navbar a {
  float: left;
  font-size: 25px;
  color: black;
  text-align: center;
  text-decoration: none;
}

.dropdown {
  float: left;
  overflow: hidden;

}

.dropdown .dropbtn {
  font-size: 25px;
  border: none;
  outline: none;
  color: black;
  background-color: inherit;
  font-family: inherit;
  margin: 15px;
  margin-top: 11px;
}

.navbar a:hover, .dropdown:hover .dropbtn {
  background-color: ghostwhite;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: ghostwhite;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content a:hover {
  background-color: lightskyblue;
}

.dropdown:hover .dropdown-content {
  display: block;
}

/* end of navbar */
</style>