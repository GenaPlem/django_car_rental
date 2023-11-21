const startDateInput = document.getElementById('id_start_date');
const endDateInput = document.getElementById('id_end_date');
const insuranceTypeSelect = document.getElementById('id_insurance_type');
const childSeatCheckbox = document.getElementById('id_child_seat');
const pricePerDayElement = document.getElementById('price_per_day');
const totalPriceElement = document.getElementById('total_price');
/**
* Function to update booking total price
*/
const updateTotalPrice = () => {
    let startDate = startDateInput.value;
    let endDate = endDateInput.value;
    let insuranceType = insuranceTypeSelect.value;
    let childSeat = childSeatCheckbox.checked;
    let pricePerDay = pricePerDayElement.textContent.match(/\d+/)[0];

    let insuranceCost = insuranceType === 'young' ? 50 : (insuranceType === 'senior' ? 60 : 40);
    let childSeatCost = childSeat ? 15 : 0;
    
    if (startDate && endDate) {
        let start = new Date(startDate);
        let end = new Date(endDate);
        let days = (end - start) / (1000 * 60 * 60 * 24) + 1;
        let total = days * +pricePerDay + insuranceCost + childSeatCost;

        totalPriceElement.textContent = total + '€';
    } else {
        let total = +pricePerDay + insuranceCost + childSeatCost;

        totalPriceElement.textContent = total + '€';
    }
}
/**
* Function to update min value of End Date after Start Date changes
*/
const updateEndDateMin = () => {
    endDateInput.setAttribute('min', startDateInput.value);
    if (startDateInput.value > endDateInput.value) {
        endDateInput.value = startDateInput.value;
        updateTotalPrice()
    }

}

/* Booking form listeners */
startDateInput.addEventListener('change', updateTotalPrice);
startDateInput.addEventListener('change', updateEndDateMin);
endDateInput.addEventListener('change', updateTotalPrice);
insuranceTypeSelect.addEventListener('change', updateTotalPrice);
childSeatCheckbox.addEventListener('change', updateTotalPrice);


updateTotalPrice()