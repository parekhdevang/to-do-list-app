DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
FIRST_DAY = new Date();

function getDateInString(date) {
    return `${MONTHS[date.getMonth() - 1]} ${date.getDate()}, ${date.getFullYear()}`;
}

function getDayInString(date) {
    return DAYS[date.getDay()];
}

function getTomorrowDate(today) {
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow;
}

function getYesterdayDate(today) {
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    return yesterday;
}

function setDates(firstDay) {
    let weekContainer = document.getElementById("week-container");
    let children = weekContainer.children;
    var date = firstDay;
    for (var i=0; i<children.length; i++) {
        if (children[i].className === "day-col") {
            let dayChildren = children[i].children;
            for (var j=0; j<dayChildren.length; j++) {
                if (dayChildren[j].className === "day-of-week") {
                    dayChildren[j].textContent = getDayInString(date);
                } else if (dayChildren[j].className === "date") {
                    let dateInStr = getDateInString(date);
                    dayChildren[j].textContent = dateInStr;
                    children[i].id = dateInStr; // set it as the id of the parent div
                }
            }
            date = getTomorrowDate(date);
        }
    }
}

function goBackADay() {
    let yesterday = getYesterdayDate(FIRST_DAY);
    setDates(yesterday);
    FIRST_DAY = yesterday;
}

function goForwardADay() {
    let tomorrow = getTomorrowDate(FIRST_DAY);
    setDates(tomorrow);
    FIRST_DAY = tomorrow;
}

setDates(FIRST_DAY);