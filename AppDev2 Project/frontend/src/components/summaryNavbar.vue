<template>
  <div class="navbar">
    <img class='logo' src='../assets/logo.webp' width=100 height=50 alt="logo">

    <div class="dropdown">
      <button class="dropbtn">
        Profile🔻
        <i class="down"></i>
      </button>
      <div class="dropdown-content">
        <router-link :to="{ name: 'Home', params: { id: this.user_id } }"> Home 🛸</router-link>
        <a href="" @click.prevent="logout"> Logout </a>
      </div>
    </div>

  </div>
</template>

<script>
import logout from "@/functions/logout.js";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "summaryNavbar",
  inheritAttrs:false,

  methods: {
    logout() {
      logout();
    },
  },

  props: {
    user_id: null,
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