<template>
  <div class="sketchy">
    <div class="card-body">
      <ul class="list-group1">
        <h3> 📎{{ this.card_title }} </h3>
        <li class="list-group1-item"> {{ this.card_content }} </li>
        <li class="list-group1-item"> {{ this.card_status }} </li>
        <li class="list-group1-item">🚨Card Deadline : {{ this.card_deadline }} </li>
      </ul>
    </div>
  </div>
</template>

<script>

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Card",
  inheritAttrs:false,

  props: {
      card_id: null,
      user_id: null,
      list_id: null,
      card_title: null,
      card_content: null,
      card_status: null,
      card_deadline: null,
  },

  methods: {
  },

}
</script>

<style scoped>
.sketchy {
  padding: 3px 3px;
  display: inline-block;
  border: 3px solid saddlebrown;
  font-size: 16px;
  font-family: monospace;
  border-radius: 2% 6% 5% 4% / 1% 1% 2% 4%;
  text-transform: uppercase;
  letter-spacing: 0.1ch;
  background: #ffffff;
  position: relative;
}

.sketchy::before {
   content: '';
   border: 2px solid #353535;
   display: block;
   width: 100%;
   height: 100%;
   position: absolute;
   top: 50%;
   left: 50%;
   transform: translate3d(-50%, -50%, 0) scale(1.015) rotate(0.5deg);
   border-radius: 1% 1% 2% 4% / 2% 6% 5% 4%;
 }

.option1 {
  float: left;
}

.option2 {
  float: right;
}
</style>