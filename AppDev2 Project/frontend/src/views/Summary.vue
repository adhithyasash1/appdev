<template>
  <navbar :user_id="this.user_id" />

  <div class="main" v-if="step1.length > 0">
    <div class="container" v-for="(item, index) in step2" :key="item.list_id">
    <div class="content">
      <div class="gradient-border" id="box">
        <bar-chart :list_name="step2[index].name" :xValues="step2[index].xValues" :yValues="step2[index].yValues" :barColors="step2[index].barColors" />
      </div>
    </div>
    </div>
  </div>

  <div class="noSummary" v-if="step1.length === 0">
    <h1 style="font-family: monospace;">Nothing to show here!</h1>
    <h3 style="font-family: monospace;">Make a list to see your summary!</h3>
  </div>

</template>

<script>
import summaryNavbar from "@/components/summaryNavbar.vue";
import dataForGetSomeData from "@/functions/cleanData";
import dataForGraphData from "@/functions/someData";
import BarChart from "@/components/Chart.vue";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Summary",
  inheritAttrs:false,

  components: {
    'navbar': summaryNavbar,
    'bar-chart': BarChart,
  },

  data() {
    return {
      user_id: this.user_id,
      step1: null,
      step2: null,
    };
  },

  async created() {
      const res = await fetch(`http://localhost:8080/api/user/summary`, {
        method: 'GET',
        mode: 'cors',
        headers: {
          'user_id' : this.user_id,
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': localStorage.getItem('Authentication-Token'),
        },
      })
      const data = await res.json()
      if (res.ok) {
        this.step1 = dataForGetSomeData(data);
        console.log(this.step1)
        this.step2 = dataForGraphData(this.step1);
      }
      else if (res.status === 401) {
        console.log(res)
      }
  },

  beforeCreate() {
    this.user_id = this.$route.params.id;
  },

}
</script>

<style scoped>
.container{
  display: flex;
  background: ghostwhite;
  cursor: pointer;
  border-radius: 15px;
  position: relative;
  padding: 30px 40px;
  margin-left: 50px;
  margin-top: 20px;
  color: var(--primary-color);
  float: left;
}

.container::after{
  content: '';
  background: var(--primary-color);
  border-radius: 15px;
  height: 100%;
  width: 100%;
  position: absolute;
  left: 0;
  top: 0;
  z-index: 0;
  clip-path: circle(5% at 0% 0%);
  transition: all .3s ease-in;
}

.content{
  position: relative;
  z-index: 1;
  transition: all .3s ease-in;
}

.container:hover::after {
  clip-path: circle(100%);
}

.container:hover .content {
  color: var(--text-color);
}


.main {
  display: inline-block;
  padding: 80px 100px;
  font-family: monospace;
}

#box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 650px;
  height:400px;
  color: black;
  font-family: monospace;
  font-size: 2.5rem;
}

.gradient-border {
  --borderWidth: 5px;
  background: ghostwhite;
  position: relative;
  border-radius: 7px;
}

.gradient-border:after {
  content: '';
  position: absolute;
  top: calc(-1 * var(--borderWidth));
  left: calc(-1 * var(--borderWidth));
  height: calc(100% + var(--borderWidth) * 2);
  width: calc(100% + var(--borderWidth) * 2);
  background: linear-gradient(60deg, saddlebrown, seagreen, skyblue, #f79533, #f37055, #ef4e7b, #a166ab, #5073b8, #1098ad, #07b39b, #6fba82);
  border-radius: calc(2 * var(--borderWidth));
  z-index: -2;
  animation: animatedgradient 2.2s ease alternate infinite;
  background-size: 300% 300%;
}


@keyframes animatedgradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

:root{
  --primary-color: sienna;
  --bg-color: #dfe6e9;
  --text-color: white;
}
</style>