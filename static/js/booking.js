/**
* Function to update booking total price
*/
function updateTotalPrice() {
    let startDate = document.getElementById('id_start_date').value;
    let endDate = document.getElementById('id_end_date').value;
    let insuranceType = document.getElementById('id_insurance_type').value;
    let childSeat = document.getElementById('id_child_seat').checked;
    
    let pricePerDay = document.getElementById('price_per_day').textContent.match(/\d+/)[0];
    let insuranceCost = insuranceType === 'young' ? 50 : (insuranceType === 'senior' ? 60 : 40);
    let childSeatCost = childSeat ? 15 : 0;
    
    if (startDate && endDate) {
        let start = new Date(startDate);
        let end = new Date(endDate);
        let days = (end - start) / (1000 * 60 * 60 * 24) + 1;
        let total = days * +pricePerDay + insuranceCost + childSeatCost;
        document.getElementById('total_price').textContent = total + '€';
    } else {
        let total = +pricePerDay + insuranceCost + childSeatCost;
        document.getElementById('total_price').textContent = total + '€';
    }
}

document.getElementById('id_start_date').addEventListener('change', updateTotalPrice);
document.getElementById('id_end_date').addEventListener('change', updateTotalPrice);
document.getElementById('id_insurance_type').addEventListener('change', updateTotalPrice);
document.getElementById('id_child_seat').addEventListener('change', updateTotalPrice);

updateTotalPrice()