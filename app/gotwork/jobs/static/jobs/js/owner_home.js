const app = Vue.createApp({
    data() {
        jobAPIURL : `http://${window.location.host}/jobsAPI`
    },

    methods: {

    },

    created() {

    }
});

const vm = app.mount("#app")