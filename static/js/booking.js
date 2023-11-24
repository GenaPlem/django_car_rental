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
    let childSeat = childSeatCheckbox ? childSeatCheckbox.checked : false;
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
    format: 'yyyy-mm-dd'
})
const endDatepicker = new Datepicker(endDateInput, {
    minDate: new Date(),
    autohide: true,
    datesDisabled: bookedDates,
    format: 'yyyy-mm-dd'
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

/**
 * Function to update max booking date for 1 month
 */
const updateEndDateMax = (e) => {
    const selectedDate = e.detail.date;
    const maxBookingDate = new Date(selectedDate.getFullYear(), selectedDate.getMonth() + 1, selectedDate.getDate());
    endDatepicker.setOptions({
        minDate: selectedDate,
        maxDate: maxBookingDate
    });

    if (endDateInput.value && new Date(endDateInput.value) < selectedDate) {
        endDatepicker.setDate(selectedDate);
    }

    if (endDateInput.value && new Date(endDateInput.value) > maxBookingDate) {
        endDatepicker.setDate(maxBookingDate)
    }
}
/* If startDateInput already has a value than max date will be after one month */
if (startDateInput.value) {
    const selectedDate = new Date(startDateInput.value);
    const maxBookingDate = new Date(selectedDate.getFullYear(), selectedDate.getMonth() + 1, selectedDate.getDate());

    endDatepicker.setOptions({
        minDate: selectedDate,
        maxDate: maxBookingDate
    });
}

/* Booking form listeners */
startDateInput.addEventListener('changeDate', updateTotalPrice);
startDateInput.addEventListener('changeDate', updateEndDateMin);
startDateInput.addEventListener('changeDate', updateEndDateMax);
endDateInput.addEventListener('changeDate', updateTotalPrice);
insuranceTypeSelect.addEventListener('change', updateTotalPrice);
if (childSeatCheckbox) {
    childSeatCheckbox.addEventListener('change', updateTotalPrice);
}


updateTotalPrice()