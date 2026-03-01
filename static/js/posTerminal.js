let lastKeyTime = Date.now();
let barcode = ""
let focusTimer
let isStageOpen = false
let cart = []
let cashBtn = document.getElementById("btn-cash");
let installmentBtn = document.getElementById("btn-installment");

document.addEventListener("keydown", (e) => {

    if (isStageOpen){
        return
    }

    const currentTime = Date.now();

    if (currentTime - lastKeyTime > 300){
        barcode = ""
    }

    lastKeyTime = currentTime;

    if (e.target.id === 'focus-qty-input') return;


    if (e.key === "Enter" || e.keyCode === 13) {
        e.preventDefault()

        if (barcode){
            console.log("Scanned Barcode: ", barcode);
            processScan(barcode);
        }

        barcode = ""
    } else {

        if (e.key.length === 1){
            barcode += e.key
        }
    }
})

async function processScan(barcode){
    const url = `/scan_product/?barcode=${barcode}`

    try{
        const response = await fetch(url);

        if (!response.ok){
            throw new Error(`Response status: ${response.status}`);
            return
        }

        const data = await response.json();

        renderFocusStage(data)

    } catch (e) {
        console.error(e)
    }
}

function addItemToCart(scannedItem) {

    const itemExist = cart.find(item => item.id === scannedItem.id);

    if (itemExist){
        itemExist.qty += scannedItem.qty
    } else {
        cart.push(scannedItem)
    }

    console.log("Cart Updated:", scannedItem);

    renderCart()
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

function renderCart(){
    const cartContainer = document.getElementById('cart-items')
    let itemName = document.getElementById('item-name')
    const totalContainer = document.getElementById('total-container')

    if (!cartContainer) return

    cartContainer.innerHTML = ''
    totalContainer.innerHTML = ''


    let totalOrderAmount = 0

    cart.forEach(item => {
        let subTotal = item.price * item.qty
        totalOrderAmount += subTotal;
        cartContainer.innerHTML += `
            <div class="flex items-center gap-4 bg-blue-800/30 p-4 rounded-2xl border border-blue-700/50">
                <img src="${item.img}" class="h-12 w-12 bg-white/10 rounded-xl flex items-center justify-center font-bold">
                <div class="flex-grow">
                    <h4 class="font-bold text-sm">${item.name}</h4>
                    <p class="text-sm text-blue-400 font-medium">Quantity: ${Number(item.qty)}</p>
                </div>
                <div class="text-right">
                    <p class="font-black text-white">₱${Number(subTotal).toLocaleString()}</p>
                </div>
            </div>
        `

        const tax = totalOrderAmount * 0.12;
        const grandTotal = totalOrderAmount + tax;

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


installmentBtn.addEventListener("mouseenter", () => {
    installmentBtn.classList.remove("bg-gray-50", "text-gray-400");
    installmentBtn.classList.add("bg-blue-950", "text-white");

    cashBtn.classList.remove("bg-blue-950", "text-white");
    cashBtn.classList.add("bg-gray-50", "text-gray-400");
});

installmentBtn.addEventListener("mouseleave", () => {
    installmentBtn.classList.remove("bg-blue-950", "text-white");
    installmentBtn.classList.add("bg-gray-50", "text-gray-400");

    cashBtn.classList.remove("bg-gray-50", "text-gray-400");
    cashBtn.classList.add("bg-blue-950", "text-white");
});