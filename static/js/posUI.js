let focusTimer

function renderCart(){
    const cartContainer = document.getElementById('cart-items')
    let itemName = document.getElementById('item-name')
    const totalContainer = document.getElementById('total-container')

    if (!cartContainer) return

    cartContainer.innerHTML = ''
    totalContainer.innerHTML = ''
    currentGrandTotal = 0

    if (cart.length === 0){
        cartContainer.innerHTML = '<p class="text-blue-400 text-center py-10">Cart is empty</p>';
        return;
    }


    let totalOrderAmount = 0

    cart.forEach(item => {
        let subTotal = item.price * item.qty
        totalOrderAmount += subTotal;
        cartContainer.innerHTML += `
                    <div class="flex items-center gap-4 bg-blue-800/30 p-4 rounded-2xl border border-blue-700/50 relative group">
                        <img src="${item.img}" class="h-12 w-12 bg-white/10 rounded-xl flex items-center justify-center font-bold">
                        
                        <div class="flex-grow">
                            <h4 class="font-bold text-sm">${item.name}</h4>
                            <p class="text-sm text-blue-400 font-medium">Quantity: ${Number(item.qty)}</p>
                        </div>
                    
                        <div class="text-right flex items-center gap-3">
                            <p class="font-black text-white">₱${Number(subTotal).toLocaleString()}</p>
                            
                            <button onclick="removeFromCart(${item.id})" 
                                    class="text-blue-400 hover:text-red-500 transition-colors font-bold text-xl px-2">
                                &times;
                            </button>
                        </div>
                    </div>
                    `

        const tax = totalOrderAmount * 0.12;
        const grandTotal = totalOrderAmount + tax;
        currentGrandTotal = grandTotal

        totalContainer.innerHTML = `
                <div class="flex justify-between text-gray-400 font-bold">
                    <span>Subtotal</span>
                    <span>${totalOrderAmount.toLocaleString()}</span>
                </div>
                <div class="flex justify-between text-gray-400 font-bold">
                    <span>Tax (12%)</span>
                    <span>₱${tax.toLocaleString()}</span>
                </div>
                <div class="flex justify-between text-2xl font-black pt-3 border-t border-gray-100">
                    <span>Total</span>
                    <span class="text-blue-700" id="total-display">₱${grandTotal.toLocaleString()}</span>
                </div>
        `

    })

}

function addItemToCart(scannedItem) {
    if (!scannedItem || !scannedItem.id || isNaN(scannedItem.price)){
        console.error("Scanned Item is invalid");
        return
    }

    const itemExist = cart.find(item => item.id === scannedItem.id);

    if (itemExist){
        itemExist.qty += scannedItem.qty
    } else {
        cart.push(scannedItem)
    }

    console.log("Cart Updated:", scannedItem);
    localStorage.setItem(cartKey, JSON.stringify(cart))

    renderCart()
}


function removeFromCart(id){
    cart = cart.filter(item => item.id !== id)

    localStorage.setItem(cartKey, JSON.stringify(cart))

    renderCart();
}


function openCheckoutModal(type){
    let modalContainer = document.getElementById('modal-container');
    let cashModal = document.getElementById("cash-modal");
    let installmentModal = document.getElementById("installment-modal");


    const cartRows = cart.map(item => {
        return `
                <div class="flex flex-row items-center justify-between border-b border-gray-100 p-2 gap-4">
                    <div class="text-left flex-grow">
                        <p class="text-sm font-bold text-gray-900">${item.name}</p>
                        <p class="text-xs text-gray-500">Qty: ${item.qty}</p>
                        <p class="text-xs font-black text-blue-600">₱${(item.price * item.qty).toLocaleString()}</p>
                        
                    </div>
                    
                    <div class="flex-shrink-0">
                        <img src="${item.img}" class="h-16 w-16 object-cover rounded-xl border border-gray-100 shadow-sm">
                    </div>
                </div>
                `
    }).join("")


    let cashModalImage = document.getElementById("cash-modal-image");



    modalContainer.classList.remove('hidden');
    installmentModal.classList.add('hidden');
    cashModal.classList.add('hidden');

    if (type === 'CASH'){
        cashModal.classList.remove('hidden');
        installmentModal.classList.add('hidden');

        cashModalImage.innerHTML = cartRows
        document.getElementById("cash-modal-price").textContent = `₱${currentGrandTotal.toLocaleString()}`;
    } else {
        cashModal.classList.add('hidden');
        installmentModal.classList.remove('hidden');

        const installmentCartItems = document.getElementById('installment-cart-items')
        const installmentTotalDisplay = document.getElementById('installment-total-display')

        installmentCartItems.innerHTML = cartRows
        installmentTotalDisplay.textContent = `₱${currentGrandTotal.toLocaleString()}`;
    }
}

function closeCheckoutModal(){
    document.getElementById('modal-container').classList.add('hidden');

    const cashRecieved = document.getElementById("cash-received");
    if (cashRecieved) {
        cashRecieved.value = ''
    }
}


function renderFocusStage(data){
    isStageOpen = true

    const inventoryGrid = document.getElementById('inventory-grid');
    const productContainer = document.getElementById('product-container');
    const focusTarget = document.getElementById('focus-card-target');

    inventoryGrid.classList.add('hidden')
    productContainer.classList.remove('hidden')

    focusTarget.innerHTML = `
        <div class="bg-white border-4 border-blue-600 rounded-[40px] shadow-2xl p-10 flex flex-col gap-6 animate-in zoom-in duration-300">
        <div class="flex items-center gap-10">
            <div class="w-40 h-40 bg-blue-50 rounded-3xl flex items-center justify-center overflow-hidden shadow-inner border-2 border-gray-100">
                    ${data.image ? `<img src="${data.image}" class="h-full w-full object-contain p-2">` : '📦'}
            </div>
            <div class="flex-grow">
                    <span class="bg-blue-600 text-white text-xs font-black px-4 py-1 rounded-full uppercase tracking-widest leading-none">
                        ${data.category || 'Product'}
                    </span>
                    <h1 class="text-5xl font-black text-gray-900 mt-2">${data.name}</h1>
                    <p class="text-blue-700 font-black text-3xl mt-1">₱${parseFloat(data.price).toLocaleString()}</p>
                </div>
            </div>
            
            <div class="flex flex-col items-center gap-2">
                    <label class="text-[10px] font-black text-gray-400 uppercase">Quantity</label>
                    <input type="number" id="focus-qty-input" value="1" min="1"
                           class="w-24 text-4xl font-black text-center p-3 bg-gray-100 border-4 border-transparent focus:border-blue-600 rounded-2xl outline-none transition-all">
            </div>
        </div>
    </div>
    `

    const qtyInput = document.getElementById('focus-qty-input');
    if(qtyInput){
        qtyInput.focus()
        qtyInput.select()

        qtyInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter'){
            clearTimeout(focusTimer)
            const qty = parseInt(qtyInput.value) || 1;
            confirmAddition(data, qty);
        }
    })
    }


    clearTimeout(focusTimer)
    focusTimer = setTimeout(() => {
        if (isStageOpen) {
            console.log("Auto-confirming...");
            qnt = qtyInput.value;
            confirmAddition(data, qnt);
        }
    }, 5000)

}

function confirmAddition(data, quantity){
    isStageOpen = false

    document.getElementById('product-container').classList.add('hidden');
    document.getElementById('inventory-grid').classList.remove('hidden');

    addItemToCart({
        id: data.id,
        name: data.name,
        price: data.price,
        qty: quantity,
        img: data.image
    });
}


function setSidebarActive(mode) {
    const cashBtn = document.getElementById("btn-cash");
    const installmentBtn = document.getElementById("btn-installment");
    const installmentOptions = document.getElementById('installment-options');

    if (!cashBtn || !installmentBtn) return;

    if (mode === 'CASH') {
        cashBtn.classList.replace("bg-gray-50", "bg-blue-950");
        cashBtn.classList.replace("text-gray-400", "text-white");

        installmentBtn.classList.replace("bg-blue-950", "bg-gray-50");
        installmentBtn.classList.replace("text-white", "text-gray-400");

        if (installmentOptions) installmentOptions.classList.add("hidden");
    } else {
        installmentBtn.classList.replace("bg-gray-50", "bg-blue-950");
        installmentBtn.classList.replace("text-gray-400", "text-white");

        cashBtn.classList.replace("bg-blue-950", "bg-gray-50");
        cashBtn.classList.replace("text-white", "text-gray-400");

        if (installmentOptions) installmentOptions.classList.remove('hidden');
    }
}

function updateInstallmentCalculation(){
    const term = parseInt(document.getElementById("inst-term").value) || 3
    const downpayment = parseFloat(document.getElementById('inst-downpayment').value) || 0

    const balance = currentGrandTotal - downpayment

    const finalBalance = Math.max(0, balance)

    const monthly = finalBalance / term

    document.getElementById('inst-balance-display').textContent = `₱${finalBalance.toLocaleString()}`
    document.getElementById('inst-monthly-display').textContent = `₱${monthly.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`


}

function calculateChange(){
    let inputCash = document.getElementById('cash-received-input')
    let changeToDisplay = document.getElementById('change-display')

    let cashRecieved = parseFloat(inputCash.value) || 0

    let change = cashRecieved - currentGrandTotal

    if(changeToDisplay){
        changeToDisplay.textContent = `₱${Math.max(0, change).toLocaleString(undefined, {minimumFractionDigits: 2})}`
        changeToDisplay.style.color = change < 0 ? "#ef4444" : "#4ade80";
    }
}



async function processCashPayment(cart, totalAmount, cashReceived, changeGiven, customerData){

    console.log("DEBUG PAYLOAD:", {cart, totalAmount, cashReceived, changeGiven});

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value

    try{

        const response = await fetch('/pos_terminal/api/checkout/cash/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },

            body: JSON.stringify({
                cart: cart,
                totalAmount: totalAmount,
                cashReceived: cashReceived,
                changeGiven: changeGiven,
                customerData: customerData,
                paymentMethod: 'CASH'
            })
        })

        const data = await response.json()

        if (data.success) {
            alert("Order #" + data.order_id + " Confirmed!")
            localStorage.removeItem(cartKey)
            cart.length = 0
            renderCart()
            closeCheckoutModal()
        } else {
            alert("Error" + data.message)
        }

    } catch (error) {
        console.error(error)
    }
}

async function processInstallmentPayment(cart, currentGrandTotal, downpayment, installmentTotal, installmentData){
    console.log("DEBUG PAYLOAD:", {cart, currentGrandTotal, downpayment, installmentTotal, installmentData})
}