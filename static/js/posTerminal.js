let barcodeBuffer = ""
let lastKeyTime = Date.now();
let barcode = ""

document.addEventListener("keydown", (e) => {

    const currentTime = Date.now();


    if (e.key === "Enter" || e.keyCode === 13) {
        e.preventDefault()

        if (barcode){
            console.log("Scanned Barcode: ", barcode);
            processScan(barcode);
        }

        barcode = ""
    } else {
        if (currentTime - lastKeyTime > 100){
            barcode = ""
        }

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
    const inventoryGrid = document.getElementById('inventory-grid');
    const productContainer = document.getElementById('product-container');
    const focusTarget = document.getElementById('focus-card-target');

    inventoryGrid.classList.add('hidden')
    productContainer.classList.remove('hidden')

    focusTarget.innerHTML += `
        <div class="bg-white border-4 border-blue-600 rounded-[40px] shadow-2xl p-10 flex flex-col gap-6 animate-in zoom-in duration-300">
        <div class="flex items-center gap-10">
            <div class="w-40 h-40 bg-blue-50 rounded-3xl flex items-center justify-center text-6xl shadow-inner">
                📦
            </div>
            <div class="flex-grow">
                <span class="bg-blue-600 text-white text-xs font-black px-4 py-1 rounded-full uppercase tracking-widest leading-none">Scanned Item</span>
                <h1 class="text-5xl font-black text-gray-900 mt-2">${data.product_name}</h1>
                <p class="text-blue-700 font-black text-3xl mt-1">₱${data.price}</p>
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
    qtyInput.focus()
    qtyInput.select()
}