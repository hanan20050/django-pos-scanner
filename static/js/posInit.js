// document.getElementById("btn-cash").addEventListener("click", () => setSidebarActive('CASH'));
// document.getElementById("btn-installment").addEventListener("click", () => setSidebarActive('INSTALLMENT'));
//
//
// checkoutBtn.addEventListener('click', () => {
//     if (cart.length === 0){
//         console.log('cart empty')
//     }
//
//     const isCashActive = document.getElementById("btn-cash").classList.contains("bg-blue-950")
//
//     openCheckoutModal(isCashActive ? 'CASH' : 'INSTALLMENT')
// })


document.addEventListener('DOMContentLoaded', () => {



    const cashBtn = document.getElementById('btn-cash')
    const installmentBtn = document.getElementById('btn-installment')
    const checkoutBtn  = document.getElementById('checkout-btn')

    if (cashBtn){
        cashBtn.addEventListener('click', () => setSidebarActive('CASH'));
    }

    if (installmentBtn){
        installmentBtn.addEventListener('click', () => setSidebarActive('INSTALLMENT'));
    }

    if (checkoutBtn){
        checkoutBtn.addEventListener('click', () => {
            if (cart.length === 0){
                console.log('cart is empyty')
                return
            }

            const isCashActive = cashBtn.classList.contains("bg-blue-950")
            openCheckoutModal(isCashActive ? 'CASH' : 'INSTALLMENT')
        })
    }

    renderCart()

    const cashInput = document.getElementById('cash-received-input');
    if (cashInput) {
        cashInput.addEventListener('input', calculateChange);
        console.log("Cash listener attached");
    }

    const placeOrderBtn = document.getElementById('place-order-btn');

    if (placeOrderBtn){
        placeOrderBtn.addEventListener('click', () => {

            const customerData = {
                name: document.getElementById('cash-cust-name').value,
                phone: document.getElementById('cash-cust-phone').value,
                email: document.getElementById('cash-cust-email').value,
                address: document.getElementById('cash-cust-address').value,
            }

            const cashReceived = document.getElementById('cash-received-input').value;
            const changeGiven = document.getElementById('change-display').innerText.replace('₱', '').replace(',', '');

            processCashPayment(cart, currentGrandTotal, cashReceived, changeGiven, customerData)
        })
    }



    const submitInstallment = document.getElementById('submit-installment')

    if (submitInstallment){
        submitInstallment.addEventListener('click', () => {

            const installmentData = {
                name: document.getElementById('ins-cust-name').value,
                email: document.getElementById('ins-cust-email').value,
                phone: document.getElementById('ins-cust-phone').value,
                address: document.getElementById('ins-cust-address').value,
                creditOfficerId: document.getElementById('ins-creditOfficer').value,
                term: document.getElementById('inst-term').value,
                downpayment: document.getElementById('inst-downpayment').value,
                balanceToFinance: document.getElementById('inst-balance-display').innerText,
                monthlyPayment: document.getElementById('inst-monthly-payment').innerText
            }

            const installmentTotal = document.getElementById('installment-total-display')

            processInstallmentPayment(cart, currentGrandTotal, installmentTotal, installmentData)
        });
    }

})