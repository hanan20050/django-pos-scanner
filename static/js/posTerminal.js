let lastKeyTime = Date.now();
let barcode = ""
let focusTimer
let isStageOpen = false

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


function renderFocusStage(data){
    isStageOpen = true

    const inventoryGrid = document.getElementById('inventory-grid');
    const productContainer = document.getElementById('product-container');
    const focusTarget = document.getElementById('focus-card-target');

    inventoryGrid.classList.add('hidden')
    productContainer.classList.remove('hidden')

    focusTarget.innerHTML = `
        <div class="bg-white border-4 border-blue-600 rounded-[40px] shadow-2xl p-10 flex flex-col gap-6 animate-in zoom-in duration-300">
<div class="flex items-center gap-8">
    ${data.image ? `
        <div class="w-48 h-48 bg-gray-50 rounded-2xl flex items-center justify-center overflow-hidden border-2 border-blue-100 shadow-sm">
            <img src="${data.image}" class="h-full w-full object-contain p-2">
        </div>
    ` : ''}

    <div class="flex-grow">
        <span class="bg-blue-600 text-white text-xs font-black px-4 py-1 rounded-full uppercase tracking-widest leading-none">
            ${data.category}
        </span>
        <h1 class="text-5xl font-black text-gray-900 mt-2">${data.name}</h1>
        <p class="text-blue-700 font-black text-3xl mt-1">₱${parseFloat(data.price).toLocaleString(undefined, {minimumFractionDigits: 2})}</p>
    </div>
</div>
    </div>
    `

    const qtyInput = document.getElementById('focus-qty-input');
    qtyInput.focus()
    qtyInput.select()

    qtyInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter'){
            clearTimeout(focusTimer)
            const qty = parseInt(qtyInput.value) || 1;
            confirmAddition(data, qty);
        }
    })

    clearTimeout(focusTimer)

    focusTimer = setTimeout(() => {
        confirmAddition(data,  1)
    }, 5000)

    qtyInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            clearTimeout(focusTimer);
            const qty = parseInt(qtyInput.value) || 1;
            confirmAddition(data, qty);
        }
    });
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

// function addItemToCart(data, quantity = 1) {
//     console.log("Adding to cart:", data, "Qty:", quantity);
//
//     // For now, let's just alert so we know it worked
//     // alert(`Added ${quantity}x ${data.name || 'Product'} to cart!`);
//
//     // Later, we will add the logic to update the blue sidebar here
// }