DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function getDateInString(date) {
    return `${MONTHS[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
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

function setDates() {
    let weekContainer = document.getElementById("week-container");
    let children = weekContainer.children;
    var date = new Date(weekContainer.className);
    for (var i=0; i<children.length; i++) {
        if (children[i].className === "day-col") {
            let dayChildren = children[i].children;
            for (var j=0; j<dayChildren.length; j++) {
                if (dayChildren[j].className === "day-of-week") {
                    dayChildren[j].textContent = getDayInString(date);
                } else if (dayChildren[j].className === "date") {
                    let dateInStr = getDateInString(date);
                    dayChildren[j].textContent = dateInStr;
                    children[i].id = date.toISOString().split('T')[0]; // set it as the id of the parent div
                }
            }
            date = getTomorrowDate(date);
        }
    }
}

function fillDateField(element) {
    let parent = element.parentNode;
    let input = document.getElementById("due_date");
    input.value = parent.id;
}

function markTaskComplete(element) {
    element.submit();
}

function submitTaskCreationForm() {
    document.getElementById("task_creation_form").submit();
}

setDates();