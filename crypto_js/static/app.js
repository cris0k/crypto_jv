/**
 * 
 * Uses cases
 * 
 */

const getTrading = (data) => {
    fetch(`http://127.0.0.1:5000/api/v1/trading/${data.crypto_from}/${data.crypto_to}/${data.amount_from}`)
        .then(response => response.json())
        .then(dataResponse => {
            document.querySelector("#amount_to").innerHTML = dataResponse.data.trading
        });
}

const getTradingHistory = () => {
    fetch(`http://127.0.0.1:5000/api/v1/trading_history`)
        .then(response => response.json())
        .then(dataResponse => {
            loadTableData(dataResponse)
        });
}

const saveExchange = (data) => {
    fetch(`http://127.0.0.1:5000/api/v1/save_exchange`,
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(dataResponse => {
            console.log(dataResponse);
            getTradingHistory()
        });
}



/**
 * 
 * Events Listener
 * 
 */

document.querySelector("#calculate").addEventListener('click', (ev) => {
    ev.preventDefault();

    const data = {
        crypto_from: document.querySelector("#crypto_from").value,
        crypto_to: document.querySelector("#crypto_to").value,
        amount_from: document.querySelector("#amount_from").value,
    }

    formValidation(data)  
        
    
    

    document.querySelector("#amount_from").addEventListener('keydown', (ev) => {
        if (ev.keyCode === 8){
            amount_to.innerHTML = "";
        };
    });
});

document.querySelector("#accept").addEventListener('click', (ev) => {
    ev.preventDefault();

    const data = {
        crypto_from: document.querySelector("#crypto_from").value,
        amount_from: document.querySelector("#amount_from").value,
        crypto_to: document.querySelector("#crypto_to").value,
        amount_to: document.querySelector("#amount_to").innerText
    }
    if(data.crypto_from === "From:"|| 
       data.crypto_to === "To:" || 
       data.amount_to === "")
       {
        alert ( "You must fill up all fields")
    }
    else{
        saveExchange(data)

    }

    
document.querySelector("#cancel").addEventListener('click', (ev) => {
    ev.preventDefault();
    data.innerHTML = "";
    });
});

document.querySelector("#btn-trades").addEventListener('click', (ev) => {
    ev.preventDefault();
    const trades = document.querySelector("#trades");
    trades.classList.toggle('is-hidden');
});


/**
 * 
 * Main
 * 
 */

 getTradingHistory()

function loadTableData(data) {
    const tbody = document.querySelector("#tbody-history");
    tbody.innerHTML = "";
    const fields = ['date', 'time', 'crypto_from', 'amount_from', 'crypto_to', 'amount_to']

    for (let i = 0; i < data.length; i++) {
        const row = document.createElement('tr')
        trading_value = data[i]
        for (const field of fields) {
            const cell = document.createElement('td')
            cell.innerHTML = trading_value[field]
            row.appendChild(cell)
        }
        tbody.appendChild(row)

    }
} 

function formValidation(data) {
    if (data.crypto_from === data.crypto_to) {
        alert('The cryptos can not be the same. Choose again')
    }
    else if(data.amount_from < 0.01 || data.amount_from === ""){
        alert("Wrong amount")
    }
    else if(data.crypto_from === "From:"|| data.crypto_to === "To:" )
       {
        alert ( "You must fill up all fields")
    }
    else {
        getTrading(data);
    }

}
