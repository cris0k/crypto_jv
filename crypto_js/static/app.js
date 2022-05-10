const getTrading = (data) => {
    fetch(`http://127.0.0.1:5000/api/v1/trading/${data.crypto_from}/${data.crypto_to}/${data.amount_from}`)
        .then(response => response.json())
        .then(dataResponse => {
            if (dataResponse.status !== 'error') {
                document.querySelector("#amount_to").innerHTML = dataResponse.data.trading
            } else {
                handlerError(dataResponse);
                document.querySelector("#amount_to").innerHTML = "";
            }
            
        });
}

const getTradingHistory = () => {
    fetch(`http://127.0.0.1:5000/api/v1/trading_history`)
        .then(response => response.json())
        .then(dataResponse => {
            if(dataResponse.status !== 'error') {
                loadTableData(dataResponse);
            } else {
                handlerError(dataResponse);
            }
            
            
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
            getTradingHistory();
            document.querySelector("#amount_from").value = 0; 
            document.querySelector("#amount_to").innerText = '';
        });
}

const myWallet = () => {
    fetch(`http://127.0.0.1:5000/api/v1/wallet`)
        .then(response => response.json())
        .then(dataResponse => {
            if(dataResponse.status !== 'error') {
                loadWallet(dataResponse);
            } else {
                handlerError(dataResponse);
            }
            
        });
}
const handlerError = (error) => {
    alert(error.message);
}



/**
 * 
 * Events Listeners
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
});

document.querySelector("#amount_from").addEventListener('keydown', (ev) => {
    if (ev.keyCode === 8){
        document.querySelector("#amount_to").innerHTML = "";
    };
});

document.querySelector("#accept").addEventListener('click', (ev) => {
    ev.preventDefault();

    const data = {
        crypto_from: document.querySelector("#crypto_from").value,
        amount_from: document.querySelector("#amount_from").value,
        crypto_to: document.querySelector("#crypto_to").value,
        amount_to: document.querySelector("#amount_to").innerText
    }
    if(data.amount_to === "")
       {
        alert ( "You must fill up all fields")
    }
    else{
        saveExchange(data)

    }
});

document.querySelector("#cancel").addEventListener('click', (ev) => {
    ev.preventDefault();
    document.querySelector("#amount_to").innerText = '';
    document.querySelector("#amount_from").value = '';
    document.querySelector("#crypto_from").value = 'From:';
    document.querySelector("#crypto_to").value = 'To:';
});

document.querySelector("#btn-trades").addEventListener('click', (ev) => {
    ev.preventDefault();
    const trades = document.querySelector("#trades");
    trades.classList.toggle('is-hidden');
});
document.querySelector("#update_wallet").addEventListener('click', (ev) => {
    ev.preventDefault();
    myWallet();
});


/**
 * 
 * Main
 * 
 */


getTradingHistory()
myWallet()

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
    else if(data.amount_from === "" || data.amount_from <= 0){
        alert("Wrong amount")
    } 
    else if(data.crypto_from ==="From:" || data.crypto_to === "To:"){
        alert("Please, fill up all fields")
    }
    else {
        getTrading(data);
    }

}
function loadWallet(data) {
    document.querySelector("#total_value").innerText = data.total_value,
    document.querySelector("#invested").innerText = data.invested,
    document.querySelector("#earnings").innerText = data.earnings

};
