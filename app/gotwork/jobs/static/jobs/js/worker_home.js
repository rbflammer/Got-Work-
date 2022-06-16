const app = Vue.createApp({
    data() {
        jobAPIURL : `http://${window.location.host}/jobsAPI`
        
    },

    methods: {
        showPopup() {
            var modal = document.getElementById("modal");
            modal.style.display = "block";
        },
        closePopup() {
            var modal = document.getElementById("modal");
            modal.style.display = "none"
        },
    },

    created() {
        
    }


});

const vm = app.mount("#app")