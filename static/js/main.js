var panel = document.querySelector("#panel");
var updatePanel = document.querySelector("#update-panel");
var warningPanel = document.querySelector("#warning");
var updateForm = document.querySelector("#update-form");

let button = document.querySelector("#add-btn");
let closeButton = document.querySelector("#close-button");
let closeUpdateButton = document.querySelector("#close-update-button");
let updateButton = document.querySelector("#update-btn");

function displayTaskInfo(taskId, taskName, taskDesc, taskStatus) {
    document.querySelector("#update_task_id").value = taskId;
    document.querySelector("#update_task_name").value = taskName;
    document.querySelector("#update_task_description").value = taskDesc;

    updatePanel.style.left = "50%";
    updatePanel.style.top = "50%";
    updatePanel.style.visibility = "visible";
}

button.addEventListener("click", () => {
    panel.style.left = "50%";
    panel.style.top = "50%";
    panel.style.visibility = "visible";
});

closeButton.addEventListener("click", () => {
    panel.style.left = "-50%";
    panel.style.top = "-50%";
    panel.style.visibility = "hidden";
});

closeUpdateButton.addEventListener("click", () => {
    updatePanel.style.left = "-50%";
    updatePanel.style.top = "-50%";
    updatePanel.style.visibility = "hidden";
});

updateButton.addEventListener("click", () => {
    updateForm.action = "/delete/" + document.querySelector("#update_task_id").value;
});