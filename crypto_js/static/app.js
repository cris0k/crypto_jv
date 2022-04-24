
  document.querySelector("#calculate").addEventListener('click', (ev) => {
    ev.preventDefault();

    const data = {
        crypto_from: document.querySelector("#crypto_from").value,
        crypto_to: document.querySelector("#crypto_to").value,
        amount_from: document.querySelector("#amount_from").value,
        
    }

    fetch(`http://127.0.0.1:5000/api/v1/trading/${data.crypto_from}/${data.crypto_to}/${data.amount_from}`)
    .then(response => response.json())
    .then(data => {
        document.querySelector("#amount_to").innerHTML = data.data.trading
    });
})

document.querySelector("#accept").addEventListener('click', (ev) => {
    ev.preventDefault();

    const data = {
        crypto_from: document.querySelector("#crypto_from").value,
        amount_from: document.querySelector("#amount_from").value,
        crypto_to: document.querySelector("#crypto_to").value,
        amount_to: document.querySelector("#amount_to").innerText
    }


    // @app.route("/api/v1/save_exchange", methods=['POST'])
    fetch(`http://127.0.0.1:5000/api/v1/save_exchange`,
    {
        method:"POST",
        body: JSON.stringify(data)
     })
    
    .then(response => response.json())
    .then(data => {
        console.log(data)
    });
})



 document.querySelector("#update_history").addEventListener('click', (ev) => {

    ev.preventDefault();

    fetch(`http://127.0.0.1:5000/api/v1/update_history`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
    });
})
