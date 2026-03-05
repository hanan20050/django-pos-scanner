// function updateInstallmentCalculation(){
//     const term = parseInt(document.getElementById("inst-term").value) || 3
//     const downpayment = parseFloat(document.getElementById('inst-downpayment').value) || 0
//
//     const balance = currentGrandTotal - downpayment
//
//     const finalBalance = Math.max(0, balance)
//
//     const monthly = finalBalance / term
//
//     document.getElementById('inst-balance-display').textContent = `₱${finalBalance.toLocaleString()}`
//     document.getElementById('inst-monthly-display').textContent = `₱${monthly.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
//
//
// }
//
// function calculateChange(){
//     let cashRecieved = parseInt(document.getElementById('cash-received-input').value)
//     let changeToDisplay = document.getElementById('change-display')
//
//     let change = cashRecieved - currentGrandTotal
//
//     if(changeToDisplay){
//         changeToDisplay.textContent = `₱${Math.max(0, change).toLocaleString(undefined, {minimumFractionDigits: 2})}`
//         changeToDisplay.style.color = change < 0 ? "#ef4444" : "#4ade80";
//     }
// }