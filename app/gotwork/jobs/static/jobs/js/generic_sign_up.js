// TODO: When the button is clicked, it has no 'being clicked' animation

var storeData = async function() {
    customer = document.getElementById('customer').checked;
    worker = document.getElementById('worker').checked;
        if (worker) {
            window.location.href = "http://localhost:8000/sign_up/worker";
        } else if (customer) {
            window.location.href = "http://localhost:8000/sign_up/customer";
        }   
    }
