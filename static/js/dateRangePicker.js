// Date Range Picker
$(function () {
    $("#scheduler").daterangepicker({
        locale: {
            format: "YYYY-MM-DD HH:mm:ss",
            separator: " ~ ",
            applyLabel: "확인",
            cancelLabel: "취소",
            fromLabel: "From",
            toLabel: "To",
            customRangeLabel: "Custom",
            weekLabel: "W",
            daysOfWeek: ["월", "화", "수", "목", "금", "토", "일"],
            monthNames: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
            firstDay: 1,
        },
        startDate: new Date(),
        endDate: new Date(),
        minDate: new Date(),
        maxSpan: {days: 7},
        drops: "up",
        timePicker: true,
        timePicker24Hour: true,
        timePickerSeconds: true,
    });
});
