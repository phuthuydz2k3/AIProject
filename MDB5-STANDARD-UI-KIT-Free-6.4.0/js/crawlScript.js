document.addEventListener("DOMContentLoaded", () => {
    const buttonURL = document.getElementsByClassName("btn-block")[0];
    const containerWeb = document.getElementsByClassName("containerWeb")[0];
    const containerScrape = document.getElementsByClassName("containerScrape")[0];
    const buttonCompany = document.getElementById("a");
    const urlVietcombanks = ["https://vneconomy.vn/dai-gia-game-vng-rot-22-5-trieu-usd-vao-funding-societies.htm"
        , "https://vneconomy.vn/start-up-telio-nhan-22-5-trieu-usd-tu-vng.htm"
        , "https://vneconomy.vn/vietcombank-xung-danh-don-vi-anh-hung.htm"
        , "https://vneconomy.vn/vietcombank-60-nam-thap-sang-niem-tin-vuon-ra-bien-lon.htm"
        , "https://vneconomy.vn/nhieu-uu-dai-lai-suat-cho-khach-hang-vay-von-tai-vietcombank-trong-thang-3-2023.htm"
        , "https://vneconomy.vn/vietcombank-va-jcb-ra-mat-the-tin-dung-quoc-te-vietcombank-jcb-platinum.htm"
        , "https://vneconomy.vn/vietcombank-giu-vung-vi-tri-ngan-hang-so-1.htm"
        , "https://vneconomy.vn/vng-lo-gan-27-ty-ngay-trong-quy-dau-tien-nam-2021.htm"
        , "https://vneconomy.vn/quy-2-2019-cong-ty-me-vng-lo-rong-102-ty-dong.htm"
        , "https://vneconomy.vn/kinh-doanh-khong-hieu-qua-vng-dong-cua-game-auto-chess-vng.htm"]

    const chartCanvas = document.getElementById('pie-chart');
    const chartCanvas2 = document.getElementById('pie-chart2');
    const chart = new Chart(chartCanvas, {
        type: 'pie',
        data: {
            labels: ["Positive", "Negative", "Neutral"],
            datasets: [{
                backgroundColor: [
                    "#254BDD",
                    "#e63946",
                    "#ffbe0b",
                ],
                data: [418, 263, 434]
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Pie Chart for admin panel'
            },
            reponsive: true
        }
    });
    const chart2 = new Chart(chartCanvas2, {
        type: 'pie',
        data: {
            labels: ["Positive", "Negative", "Neutral"],
            datasets: [{
                backgroundColor: [
                    "#254BDD",
                    "#e63946",
                    "#ffbe0b",
                ],
                data: [418, 263, 434]
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Pie Chart for admin panel'
            },
            reponsive: true
        }
    });

    const ul = document.getElementsByClassName("anchors")[0];

    urlVietcombanks.forEach(url => {
        const li = document.createElement("li")
        li.innerHTML = url
        ul.appendChild(li)
    })


    const loadSpecificWebsite = () => {
        const url = document.getElementById('typeURL').value;

        containerWeb.innerHTML = "";
        containerScrape.style.backgroundColor = "#10162F"

        const iframe = document.createElement("iframe");
        iframe.src = url;

        containerWeb.appendChild(iframe);
    }

    async function scrapeWebsite(event) {
        const url = document.getElementById('typeURL').value;

        event.preventDefault();
        if (url === "") {
            return;
        }

        const formData = new URLSearchParams();
        formData.append('url', url);

        try {
            const response2 = await fetch('http://127.0.0.1:5000/sentiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            });
            const result = await response2.text();
            const numberArray = result.split(' ').map(str => parseFloat(str));

            chart.data.datasets[0].data = numberArray;
            chart.update();

            const num1 = document.getElementById("num1");
            const num2 = document.getElementById("num2");
            const num3 = document.getElementById("num3");
            num1.innerHTML = numberArray[0].toString() + "%";
            num2.innerHTML = numberArray[1].toString() + "%";
            num3.innerHTML = numberArray[2].toString() + "%";
        } catch (error) {
            console.error(error);
        }
    }

    const handleClick = (event) => {
        loadSpecificWebsite();
        scrapeWebsite(event);
    }

    buttonURL.addEventListener("click", handleClick);

    const scrapeArticle = async (url, chart) => {
        const formData1 = new URLSearchParams();
        formData1.append('url', url);

        try {
            const response = await fetch('http://127.0.0.1:5000/sentiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData1,
            });
            const result1 = await response.text();
            const numberArray1 = result1.split(' ').map(str => parseFloat(str));

            chart.data.datasets[0].data = numberArray1;
            chart.update();

            const num1 = document.getElementById("num11");
            const num2 = document.getElementById("num22");
            const num3 = document.getElementById("num33");
            num1.innerHTML = numberArray1[0].toString() + "%";
            num2.innerHTML = numberArray1[1].toString() + "%";
            num3.innerHTML = numberArray1[2].toString() + "%";
        } catch (error) {
            console.error(error);
        }
    }

    const printCompanyArticle = async (event) => {
        const ul = document.getElementsByClassName("anchors")[0];
        ul.innerHTML = "";
        event.preventDefault();

        const company = document.getElementById("typeCompany").value;
        const formData2 = new URLSearchParams();
        formData2.append('company', company);

        try {
            const response = await fetch('http://127.0.0.1:5000/sentimentCompany', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData2,
            });
            const result2 = await response.text();
            const numberArray2 = result2.split(' ').map(str => parseFloat(str));

            chart2.data.datasets[0].data = numberArray2;
            chart2.update();

            const num1 = document.getElementById("num11");
            const num2 = document.getElementById("num22");
            const num3 = document.getElementById("num33");
            num1.innerHTML = numberArray2[0].toString() + "%";
            num2.innerHTML = numberArray2[1].toString() + "%";
            num3.innerHTML = numberArray2[2].toString() + "%";
        } catch (error) {
            console.error(error);
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/sentimentPrintLinks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData2,
            });

            const urls = await response.json();

            urls.forEach(url => {
                const li = document.createElement("li")
                li.innerHTML = url
                li.addEventListener("click", () => {
                    scrapeArticle(url, chart2)
                })
                ul.appendChild(li)
            })
        } catch (error) {
            console.error(error);
        }
    }

    const handleCompany = (event) => {
        printCompanyArticle(event);
    }

    buttonCompany.addEventListener("click", handleCompany);

    const buttonDatabase = document.getElementById("b");
    buttonDatabase.addEventListener("click", async () => {
        const positiveLinks = document.getElementById("positiveLinks").value.split(/\s+/).join('\n');
        const neutralLinks = document.getElementById("neutralLinks").value.split(/\s+/).join('\n');
        const negativeLinks = document.getElementById("negativeLinks").value.split(/\s+/).join('\n');
        const formData = new URLSearchParams();
        formData.append('positiveLinks', positiveLinks);
        formData.append('neutralLinks', neutralLinks);
        formData.append('negativeLinks', negativeLinks);

        try {
            const response = await fetch('http://127.0.0.1:5000/database', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            });

            const r = await response.text();
            console.log(r); // This will log the response text from the server
        } catch (error) {
            console.error(error);
        }
    });

});
