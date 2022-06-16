const app = Vue.createApp({
    data() {

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
        addRefundRequest() {
            // Creates the refund request input block if the user did not like the job done
            let newP = document.getElementById('requestP');
            if (!newP) {
                let breakpoint = document.getElementById('break');
                let parent = document.getElementById('parent');
                
                let p = document.createElement('p');
                p.setAttribute('style', 'font-size: 20px; padding-top: 50px;');
                p.setAttribute('id', 'requestP');
                p.textContent = "Please Fill This Out If You'd Like To Send a Refund Request (Not Required)";
                parent.insertBefore(p, breakpoint);

                let input = document.createElement('input');
                input.setAttribute('type', 'text');
                input.setAttribute('name', 'refund');
                input.setAttribute('id', 'refund');
                input.setAttribute('placeholder', 'I want a refund, because...');
                input.setAttribute('class', 'refund-input');
                input.setAttribute('id', 'requestInput');
                input.setAttribute('name', 'reason');
                parent.insertBefore(input, breakpoint);

                let br = document.createElement('br');
                parent.insertBefore(br, breakpoint);

                let text = document.createElement('label');
                text.setAttribute('id', 'blacklistText');
                text.textContent = "Blacklist Worker";
                parent.insertBefore(text, breakpoint);

                let blacklist = document.createElement('input');
                blacklist.setAttribute('type', 'checkbox');
                blacklist.setAttribute('name', 'blacklist');
                blacklist.setAttribute('id', 'blacklist');
                text.appendChild(blacklist);
                parent.insertBefore(text, breakpoint);
            }
        },
        removeRefundRequest() {
            // Removes the refund request block if user changes their mind
            let newP = document.getElementById('requestP');
            if (newP) {
                let newInput = document.getElementById('requestInput');
                let parent = document.getElementById('parent');
                let blacklist = document.getElementById('blacklistText');
                parent.removeChild(newP);
                parent.removeChild(newInput);
                parent.removeChild(blacklist);
            }
        }
    },

    created() {
        
    }


});

const vm = app.mount("#app")