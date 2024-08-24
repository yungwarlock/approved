
const messageList = document.querySelectorAll(".message-item");

messageList.forEach((message) => {
  message.querySelector(".message-delete").addEventListener("click", () => {
    message.remove();
  });
});


