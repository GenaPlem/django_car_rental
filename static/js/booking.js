const startDateInput = document.getElementById('id_start_date');
const endDateInput = document.getElementById('id_end_date');
const insuranceTypeSelect = document.getElementById('id_insurance_type');
const childSeatCheckbox = document.getElementById('id_child_seat');
const carSeats = document.getElementById('car_seats');
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

/* JS Vanilla Datepicker */
const startDatepicker = new Datepicker(startDateInput, {
    minDate: new Date(),
    autohide: true,
    datesDisabled: bookedDates,
})
const endDatepicker = new Datepicker(endDateInput, {
    minDate: new Date(),
    autohide: true,
    datesDisabled: bookedDates,
})

/**
 * Function to update min value of End Date after Start Date changes
 */
const updateEndDateMin = (e) => {
    const selectedDate = e.detail.date;
    endDatepicker.setOptions({minDate: selectedDate});

    if (endDateInput.value && new Date(endDateInput.value) < selectedDate) {
        endDatepicker.setDate(selectedDate);
    }
}

/* Function, If car's seats less than 4 than user can't add a child seat */
const isChildSeatAvailable = () => {
    if (Number(carSeats.textContent.split(' ')[1]) < 4) {
        childSeatCheckbox.setAttribute('disabled', 'true')
    }
}

/* Booking form listeners */
startDateInput.addEventListener('changeDate', updateTotalPrice);
startDateInput.addEventListener('changeDate', updateEndDateMin);
endDateInput.addEventListener('changeDate', updateTotalPrice);
insuranceTypeSelect.addEventListener('change', updateTotalPrice);
childSeatCheckbox.addEventListener('change', updateTotalPrice);


isChildSeatAvailable()
updateTotalPrice()