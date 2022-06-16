var submitButton = document.getElementById('submit');
submitButton.addEventListener('click', function (event){
    let type = document.getElementById("type");
    let date = document.getElementById("date");
    let time = document.getElementById("time");
    let address = document.getElementById("address");
    let zip = document.getElementById("zip");
    let price = document.getElementById("price");

    if (!Date.parse(date.value) || !time.value || !address.value || !zip.value || !price.value || !type.value) {
        alert("All fields are required.");
    } else {
        let jobdiv = document.getElementById("jobdiv")

        let newdiv = document.createElement("div");
        newdiv.style.textAlign = "center";
        newdiv.className = "green";
        jobdiv.appendChild(newdiv);

        let header = document.createElement("h2");
        header.textContent = type.value + " for " + date.value;
        newdiv.appendChild(header);

        let details = document.createElement("pre");
        details.textContent = "Time: " + time.value + "\nAddress: " + address.value + "\nZip Code: " + zip.value + "\nPrice: " + price.value;
        newdiv.appendChild(details);
    }
})


var clearButton = document.getElementById("clear")
clearButton.addEventListener('click', function(event){
    type.value = "Snow Removal";
    date.value = "";
    time.value = "";
    address.value = "";
    zip.value = "";
    price.value = "";
})