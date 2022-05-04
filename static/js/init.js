$(function () {
    setInterval(
        (function init() {
            // 현재 시간 출력
            const recordingTime = new Date();
            $("#presentTime").text(recordingTime.toLocaleString());

            // 녹화 시간 출력
            const startTimeOfRecord = localStorage.getItem("startTimeOfRecord");
            if (startTimeOfRecord) {
                const parsedRecordTime = parseInt(startTimeOfRecord);

                const hours = parseInt(((recordingTime - parsedRecordTime) / 1000 / 60 / 60) % 60);
                const minutes = parseInt(((recordingTime - parsedRecordTime) / 1000 / 60) % 60);
                const seconds = parseInt(((recordingTime - parsedRecordTime) / 1000) % 60);
                const text = `${hours > 10 ? `0${hours}` : hours}:${minutes < 10 ? `0${minutes}` : minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;

                $("#recordingClock").text(text);
            }

            // 데이터 차트 가져오기
            // $.ajax({
            //     type: "get",
            //     url: "/data_chart",
            //     dataType: "json",
            //     success: function (result) {
            //         $("#dataChart").html(JSON.stringify(result, null, 4));
            //     },
            //     error: function () {
            //         console.log("data chart fail");
            //     },
            // });
            return init;
        })(),
        1000
    );

    // 녹화 시작 버튼
    $("#recordStart").click(function () {
        const startTimeOfRecord = Date.now();
        localStorage.setItem("startTimeOfRecord", startTimeOfRecord);
    });

    // 녹화 종료 버튼
    $("#recordStop").click(function () {
        localStorage.clear();
    });

    // 모달 창 열기
    $("#storageButton").click(function () {
        $.ajax({
            type: "get",
            url: "/get_images",
            success: function () {
                // 모달 창을 새로고침하여 데이터를 가져온다.
                $("#modal").load(window.location.href + " #modal");
            },
            error: function () {
                console.log("get images fail");
            },
        });
    });
});