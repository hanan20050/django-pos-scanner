let lastKeyTime = Date.now();
let barcode = ""

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

        if (e.key && e.key.length === 1){
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