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
})