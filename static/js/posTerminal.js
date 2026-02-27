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
    const url = `/scan_product/${barcode}`

    try{
        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok){
            throw new Error(`Response status: ${response.status}`);
        }

    } catch (e) {
        console.error(e)
    }
}